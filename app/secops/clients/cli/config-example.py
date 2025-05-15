CYBERARK = {
    "tlsVerify": 0,
    "baseurl": "https://cyberark.local/PasswordVault/api/",
    "username": "username",

    "ccpBaseurl": "https://cyberark.local/AIMWebService/api/",
    "ccpAppId": "appId",
    "ccpUsername": "username"
}

CONJUR = {
    "tlsVerify": 0,
    "baseurl": "https://conjur.local/",
    "account": "account",
    "username": "username",
    "password": "password"
}

KUBERNETES = {
    "baseurl": "https://kubernetes.local/",
    "certificateAuthorityData": "certificateAuthority", # openssl s_client --showcerts --connect kubernetes.local:6443 < /dev/null 2> /dev/null | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' | base64 -w0
    "clientCertificateData": "certificateAuthority",
    "clientKeyData": "certificateAuthority"
}

GIT = {
    "remote": "git@github.com:organization/repository.git",
    "repoKey": "|1|xxx=|xxx= ssh-ed25519 xxx",  # remote's trusted SSH public key, from /home/user/.ssh/known_hosts.
    "userKeyBase64": "xxx="  # user's private SSH key.
}
