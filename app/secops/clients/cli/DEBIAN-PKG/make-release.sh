#!/bin/bash

set -e

function System()
{
    base=$FUNCNAME
    this=$1

    # Declare methods.
    for method in $(compgen -A function)
    do
        export ${method/#$base\_/$this\_}="${method} ${this}"
    done

    # Properties list.
    ACTION="$ACTION"
}

# ##################################################################################################################################################
# Public
# ##################################################################################################################################################

#
# Void System_run().
#
function System_run()
{
    if [ "$ACTION" == "deb" ]; then
        System_definitions
        System_cleanup

        System_debianFilesSetup

        System_codeCollect
        System_codeConfig
        System_codeFilesPermissions

        System_debCreate
        System_cleanup

        echo "Created /tmp/$projectName.deb"
    fi
}

# ##################################################################################################################################################
# Private static
# ##################################################################################################################################################

function System_definitions()
{
    declare -g debPackageRelease

    declare -g projectName
    declare -g workingFolder
    declare -g workingFolderPath

    if [ -f DEBIAN-PKG/deb.release ]; then
        # Get program version from the release file.
        debPackageRelease=$(echo $(cat DEBIAN-PKG/deb.release))
    else
        echo "Error: deb.release missing."
        echo "Usage: bash DEBIAN-PKG/make-release.sh --action deb"
        exit 1
    fi

    projectName="armonisya_${debPackageRelease}_all"
    workingFolder="/tmp"
    workingFolderPath="${workingFolder}/${projectName}"
}


function System_cleanup()
{
    if [ -n "$workingFolderPath" ]; then
        if [ -d "$workingFolderPath" ]; then
            rm -fR "$workingFolderPath"
        fi
    fi
}


function System_codeCollect()
{
    mkdir -p $workingFolderPath/usr/lib/api-secops

    # Copy files.
    cp -R ../../../api $workingFolderPath/usr/lib/api-secops/
    cp -R ../../../secops $workingFolderPath/usr/lib/api-secops/

    if [ -f ../../../license.txt ]; then
        cp ../../../license.txt $workingFolderPath/usr/lib/api-secops/
    fi

    mkdir -p $workingFolderPath/var/log/secops-client

    # Remove __pycache__ folders.
    rm -fR $(find $workingFolderPath/usr/lib/api-secops/ -name __pycache__)

    rm -fR $workingFolderPath/usr/lib/api-secops/secops/clients/cli/DEBIAN-PKG
    rm -fR $workingFolderPath/usr/lib/api-secops/secops/clients/cli/RH-PKG
    rm -fR $workingFolderPath/usr/lib/api-secops/secops/clients/cli/client.log
    mv -f $workingFolderPath/usr/lib/api-secops/secops/clients/cli/config-example.py $workingFolderPath/usr/lib/api-secops/secops/clients/cli/config.py

    rm -fR $workingFolderPath/usr/lib/api-secops/api/settings_development.py
    rm -fR $workingFolderPath/usr/lib/api-secops/secops/sql/secops.data-development.sql

    echo "JWT_TOKEN = {\"publicKey\": \"\"}" > $workingFolderPath/usr/lib/api-secops/api/settings_jwt.py
}


function System_codeConfig()
{
    # Clean settings.
    sed -i "s/^SECRET_KEY =.*/SECRET_KEY = \"not.used\"/g" $workingFolderPath/usr/lib/api-secops/api/settings.py
}


function System_codeFilesPermissions()
{
    # Forcing standard permissions (755 for folders, 644 for files, owned by root:root).
    chown -R 0:0 $workingFolderPath/usr/lib/api-secops
    find $workingFolderPath/usr/lib/api-secops -type d -exec chmod 0755 {} \;
    find $workingFolderPath/usr/lib/api-secops -type f -exec chmod 0644 {} \;

    touch $workingFolderPath/var/log/secops-client/client.log
    chmod 770 $workingFolderPath/var/log/secops-client
    chmod 660 $workingFolderPath/var/log/secops-client/client.log
}


function System_debianFilesSetup()
{
    mkdir -p $workingFolderPath

    # Setting up all the files needed to build the package (DEBIAN folder).
    cp -R DEBIAN-PKG/DEBIAN $workingFolderPath

    sed -i "s/^Version:.*/Version:\ $debPackageRelease/g" $workingFolderPath/DEBIAN/control

    if [ -f $workingFolderPath/DEBIAN/preinst ]; then
        chmod +x $workingFolderPath/DEBIAN/preinst
    fi
    if [ -f $workingFolderPath/DEBIAN/postinst ]; then
        chmod +x $workingFolderPath/DEBIAN/postinst
    fi
    if [ -f $workingFolderPath/DEBIAN/prerm ]; then
        chmod +x $workingFolderPath/DEBIAN/prerm
    fi
    if [ -f $workingFolderPath/DEBIAN/postrm ]; then
        chmod +x $workingFolderPath/DEBIAN/postrm
    fi
}


function System_debCreate()
{
    cd $workingFolder
    dpkg-deb --build $projectName
}

# ##################################################################################################################################################
# Main
# ##################################################################################################################################################

ACTION=""

# Must be run as root.
ID=$(id -u)
if [ $ID -ne 0 ]; then
    echo "This script needs root powers."
    exit 1
fi

# Parse user input.
while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        --action)
            ACTION="$2"
            shift
            shift
            ;;

        *)
            shift
            ;;
    esac
done

if [ -z "$ACTION" ]; then
    echo "Missing parameters. Use --action deb."
else
    System "system"
    $system_run
fi

exit 0
