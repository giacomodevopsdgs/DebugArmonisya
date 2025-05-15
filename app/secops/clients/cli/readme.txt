CLI MODE
^^^^^^^^

Installation:
    Via Linux standard package (deb, rpm)
        System must reach the Python pip repositories
    Project path: /usr/lib/api-secops


Configuration:
    * /usr/lib/api-secops/secops/clients/cli/config.py
    * CCP
        Client-side certification-based authentication:
            put .crt + .key client certificates in /usr/lib/api-secops/secops/clients/certificates/
            The certificate files must be unencrypted

            From pkcs12:
                openssl pkcs12 -in filename.pfx -nocerts -out filename.key -nodes
                openssl pkcs12 -in filename.pfx -clcerts -nokeys -out filename.crt -nodes


Run:
    cd /usr/lib/api-secops/secops/clients/cli

    CREATE:
    python bper-client.py --action insert --safeName BPER__SAFE_1 --safeMember LOB_Demo --accountsDescriptionJsonFile /tmp/accounts
        /tmp/accounts
        [
            {
                "platform": "BPER_DummyPlatform",
                "address": "-",
                "name": "db_password_user.123456.1",
                "userName": "user1",
                "secret": "aVerySecretSecret1",
                "encoded": false,
                "key": "db_password"
            }
        ]

    ASSOCIATE:
    python bper-client.py --action associate --safeName BPER__SAFE_1 --safeMember LOB_Demo --accountsDescriptionJsonFile /tmp/associate --vaultName VaultDemo --appName pba2-be --appNamespace pba2-svil-evo --ticket TICKET01
    /tmp/associate
    [
        {
            "uuid": "194_3@1744793613",
            "slot": "auto",
            "force": false
        },
        {
            "uuid": "194_4@1744793615",
            "slot": "auto",
            "force": false
        },
        {
            "uuid": "194_5@1744793617",
            "slot": "auto",
            "force": false
        }
    ]

    python bper-client.py --cyberark "safes list"


Logs:
    Log file in /var/log/secops-client/client.log
        * add user who will run the script to the secops group: usermod -a -G secops <user>
        * chmod g+w /var/log/secops-client/client.log
