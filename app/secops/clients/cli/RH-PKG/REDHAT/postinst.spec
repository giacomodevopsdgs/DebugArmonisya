%post
#!/bin/bash

printf "\n* Configuring Python...\n"
update-alternatives --install /usr/bin/pip pip /usr/bin/pip3.11 1
update-alternatives --set pip /usr/bin/pip3.11

update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1
update-alternatives --set python /usr/bin/python3.11

breakSystemPackages=""
pip install djangorestframework~=3.14.0 $breakSystemPackages
pip install pyyaml~=6.0.2 $breakSystemPackages
pip install GitPython~=3.1.43 $breakSystemPackages
pip install kubernetes~=32.0.1 $breakSystemPackages

chown -R root:secops /var/log/secops-client

exit 0
