import os
import pathlib
import base64
import yaml

from secops.models.Conjur.Policy import Policy
from secops.models.Conjur.Apikey import Apikey
from secops.models.Kubernetes.Secret import Secret

from secops.helpers.Log import Log
from secops.helpers.Filesystem import Filesystem
from secops.helpers.GitSupplicant import GitSupplicant


class Conjur:
    def __init__(self, sessionUid: str, **params):
        self.sessionUid: str = sessionUid
        self.assets = params.get("assets", {})
        self.vault = params.get("vault", {}).get("name", "")
        self.conjurData = params.get("conjur", {})

        self.git = GitSupplicant(asset=self.assets.get("git", {}))



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def __call__(self, action: str) -> None:
        try:
            if action == "align-git-policy":
                self._conjurPolicyApply(f"{self.git.getLocalRepo()}/nodo-conjur/conjur/automation")
                self._k8sConfig(
                    path=f"{self.git.getLocalRepo()}/nodo-conjur/devops",
                    apiKey=self._conjurApiKeyRotate()
                )
            elif action == "verify-git-policy":
                self._verifyConfig(path=f"{self.git.getLocalRepo()}/nodo-conjur/devops")
            else:
                raise NotImplemented
        except Exception as e:
            raise e



    ####################################################################################################################
    # Protected methods
    ####################################################################################################################

    def _conjurPolicyApply(self, path: str) -> None:
        #   Apply policy files recursively found, with branch as folder name
        #   (except for /project-grants/* which is named after vault name).
        #   ├── environments
        #   │   └── kubernetes
        #   │       └── automation
        #   │           ├── grants
        #   │           │   └── project-grants
        #   │           │       └── demo-app.yml
        #   │           └── projects
        #   │               └── demo-app.yml
        #   └── root
        #       └── policies.yml

        try:
            for filePath in Filesystem.files(path):
                fileSubPath = filePath.replace(path, "")
                if pathlib.Path(fileSubPath).suffix == ".yml":
                    branch = os.path.dirname(fileSubPath)

                    if "/project-grants" in branch:
                        Policy.add(
                            asset=self.assets.get("conjur", {}),
                            sessionUid=self.sessionUid,
                            data=Filesystem.fileRead(filePath),
                            parentId=self.vault
                        )
                    else:
                        Policy.add(
                            asset=self.assets.get("conjur", {}),
                            sessionUid=self.sessionUid,
                            data=Filesystem.fileRead(filePath),
                            parentId=branch
                        )
        except Exception as e:
            raise e



    def _conjurApiKeyRotate(self) -> str:
        try:
            return Apikey.rotate(
                asset=self.assets.get("conjur", {}),
                sessionUid=self.sessionUid,
                id="host:" + self.conjurData.get("hostId")
            )
        except Exception as e:
            raise e



    def _k8sConfig(self, path: str, apiKey: str) -> None:
        try:
            # Modify files.
            # └── devops
            #     ├── cluster-secret-store
            #     │    ├── cluster-secret-store-template
            #     │    └── secret-secretstore-template
            #     ├── externalsecret
            #     │    └── external-secret-template
            #     └── k8s-config
            #         └── namespace.yml

            # ├── cluster-secret-store/.
            clusterSecretStore = Filesystem.fileRead(
                f"{path}/cluster-secret-store/cluster-secret-store-template").replace(
                "__cabunndlebase64__", self.conjurData.get("caBundleBase64")
            )

            secretSecretStore = Filesystem.fileRead(f"{path}/cluster-secret-store/secret-secretstore-template").replace(
                "__hostidbase64__", str(base64.b64encode(self.conjurData.get("hostId").encode("utf-8")).decode("utf-8"))
            ).replace(
                "__apikeybase64__", str(base64.b64encode(apiKey.encode("utf-8")).decode("utf-8"))
            )

            # ├── externalsecret/.
            externalSecret = Filesystem.fileRead(f"{path}/externalsecret/external-secret-template").replace(
                "__conjurvariable__", self.conjurData.get("variable")
            )

            # └── k8s-config/.
            namespace = Filesystem.fileRead(f"{path}/k8s-config/namespace.yml")

            # Push to repo.
            self.__gitPush(path=path, clusterSecretStore=clusterSecretStore, externalSecret=externalSecret, namespace=namespace)

            # Set k8s Secret.
            self.__setKubernetesSecret(secretSecretStore=secretSecretStore)

        except Exception as e:
            raise e



    def _verifyConfig(self, path: str) -> None:
        try:
            externalSecretInfo = yaml.safe_load(
                Filesystem.fileRead(f"{path}/externalsecret/external-secret-template")
            )

            self.__getKubernetesSecret(
                secret=externalSecretInfo.get("metadata", {}).get("name", ""),
                namespace=externalSecretInfo.get("metadata", {}).get("namespace", "")
            )
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __gitPush(self, path: str, clusterSecretStore: str, externalSecret: str, namespace: str) -> None:
        try:
            k8sFilesToGit = [
                ("cluster-secret-store/cluster-secret-store.yaml", "clusterSecretStore"),
                ("externalsecret/external-secret.yml", "externalSecret"),
                ("k8s-config/namespace.yml", "namespace")
            ]
            for configFile in k8sFilesToGit:
                Log.actionLog(f"[USE CASE] File: {configFile[0]}\r\n + {eval(configFile[1])}")

                with open(f"{path}/{configFile[0]}", mode="w") as f:
                    f.write(eval(configFile[1]))

            Log.actionLog(f"[USE CASE] Pushing to git repo...")
            self.git.commit(commitMessage="Something to be decided")
            self.git.push()
        except Exception as e:
            raise e



    def __setKubernetesSecret(self, secretSecretStore: str) -> None:
        try:
            # @todo: verify.

            secretSecretStoreObject = yaml.safe_load(secretSecretStore)
            Secret.add(
                name=secretSecretStoreObject.get("metadata", {}).get("name", ""),
                namespace="automation-demo",
                data={
                    "apikey": secretSecretStoreObject.get("data", {}).get("apikey", ""), # already base64-encoded.
                    "hostid": secretSecretStoreObject.get("data", {}).get("hostid", "") # already base64-encoded.
                },
                asset=self.assets.get("kubernetes", {})
            )
        except Exception as e:
            raise e



    def __getKubernetesSecret(self, secret: str, namespace: str) -> None:
        try:
            # @todo: broken?

            Secret(name=secret, namespace=namespace, asset=self.assets.get("kubernetes", {}))
        except Exception as e:
            raise e
