from typing import Union

import os
import re
import yaml

from secops.models.CyberArk.Safe import Safe
from secops.models.CyberArk.Account import Account

from secops.helpers.Log import Log
from secops.helpers.GitSupplicant import GitSupplicant
from secops.helpers.Exception import CustomException


class BPER:
    def __init__(self, sessionUid: str, **params):
        self.sessionUid: str = sessionUid

        self.__validate([
            (params["app"], "no-uppercase"),
            (params["app"], "no-at-pipe")
        ])
        self.params = params



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def __call__(self, action: str) -> Union[list, dict, None]:
        msg = None
        result = []

        try:
            if action == "cyberark-insert":
                return self._cyberArkInsert()

            elif action == "cyberark-modify":
                try:
                    result = self._cyberArkModify()
                except CustomException as e:
                    # On Custom 409, proceed with Kubernetes step, but return a message.
                    if e.status == 409:
                        msg = e.payload
                    else:
                        raise e

                self._kubernetes()

                if msg:
                    return msg
                else:
                    return result
            else:
                raise NotImplemented
        except Exception as e:
            raise e
        
        # @todo: serializer:
        # STEP 1:
        #     "data": {
        #         "safe": {
        #             "name": "BPER__SAFE_1",
        #             "description": "This is the description for the Safe",       # optional
        #             "member": "LOB_Demo"
        #         },
        #         "accounts": [
        #             {
        #                 "platform": "BPER_DummyPlatform",
        #                 "address": "-",
        #                 "name": "db_password_user.123456.1",
        #                 "userName": "user1",
        #                 "secret": "aVerySecretSecret1",
        #                 "encoded": false,
        #                 "key": "db_password"
        #             }
        #         ]
        #     }

        # STEP 2:
        #     "data": {
        #         "vault": {
        #             "name": "VaultDemo"
        #         },
        #         "safe": {
        #             "name": "BPER__SAFE_1",
        #             "member": "LOB_Demo"
        #         },
        #         "accounts": [
        #             {
        #                 "uuid": "183_3@1743756407",
        #                 "slot": "auto",
        #                 "force": false
        #             }
        #         ],
        #         "app": {
        #             "name": "pba2-be",
        #             "namespace": "pba2-svil-evo"
        #         },
        #         "ticket": "TICKET001"
        #     }



    ####################################################################################################################
    # Protected methods
    ####################################################################################################################

    def _cyberArkInsert(self) -> list:
        try:
            asset = self.params.get("assets", {}).get("cyberark", {})
            if asset:
                # Create CyberArk Safe and add Member.
                self.__createCyberArkSafe(asset=asset)
                self.__addCyberArkMemberToSafe(asset=asset)

                # Create CyberArk Account (secret) and add to Safe.
                o = self.__addCyberArkAccounts(asset=asset)

                # @note: rollback in case of failure not necessary.
            else:
                raise CustomException(status=400)
        except Exception as e:
            raise e

        return o



    def _cyberArkModify(self) -> list:
        try:
            asset = self.params.get("assets", {}).get("cyberark", {})
            if asset:
                return self.__modifyCyberArkAccounts(asset=asset)
            else:
                raise CustomException(status=400)
        except Exception as e:
            raise e



    def _kubernetes(self) -> None:
        validAccounts = []

        try:
            # Fetch account information from CyberArk.
            # Get account information for the accounts selected by the user (via Mapping).
            cyberArkAsset = self.params.get("assets", {}).get("cyberark", {})
            if cyberArkAsset:
                accounts = Account.rawDataList(cyberArkAsset, self.params["safe"]["name"], sessionUid=self.sessionUid)

                for account in accounts:
                    if f"|{self.params['app']['name']}@" in account.get("platformAccountProperties", {}).get("Mapping", ""):
                        validAccounts.append(account)

                # Write to Kubernetes.
                gitAssetInformation = self.params.get("assets", {}).get("git", {})
                if gitAssetInformation:
                    git = GitSupplicant(asset=gitAssetInformation)
                    localRepoFolder = f"{git.getLocalRepo()}/devops/{self.params['app']['name']}"

                    # /k8s-config.
                    k8sFolder = f"{localRepoFolder}/k8s-config/"
                    if not os.path.exists(k8sFolder):
                        os.makedirs(k8sFolder)

                    self.__saveK8sConfigFiles(accountsMappedToTheApplication=validAccounts, path=k8sFolder)

                    # Push to repo.
                    Log.actionLog(f"[USE CASE] Pushing to git repo")
                    git.commit(commitMessage=self.params.get("ticket", "Automated commit"))
                    git.push()
                else:
                    raise CustomException(status=400)
            else:
                raise CustomException(status=400)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods, CyberArk
    ####################################################################################################################

    def __createCyberArkSafe(self, asset: dict) -> None:
        Log.actionLog(f"[USE CASE] Creating Safe {self.params['safe']['name']}")

        try:
            Safe.add(
                asset=asset,
                data={
                    "managingCPM": "passwordManager",
                    "safeName": self.params["safe"]["name"],
                    "description": self.params["safe"].get("description", ""),
                    "location": "\\",
                    "numberOfDaysRetention": 0
                },
                sessionUid=self.sessionUid
            )
        except CustomException as e:
            if e.status == 409:
                pass # re-use existing Safes.
            else:
                raise e
        except Exception as e:
            raise e



    def __addCyberArkMemberToSafe(self, asset: dict) -> None:
        Log.actionLog(f"[USE CASE] Creating Member {self.params['safe']['member']} and adding to Safe {self.params['safe']['name']}")

        try:
            Safe(asset=asset, id=self.params["safe"]["name"], sessionUid=self.sessionUid).addMember(
                data={
                    "memberName": self.params["safe"]["member"],
                    "memberType": "User",
                    "isExpiredMembershipEnable": False,
                    "isPredefinedUser": False,
                    "isReadOnly": True,
                    "permissions": {
                        "useAccounts": True,
                        "retrieveAccounts": True,
                        "listAccounts": True,
                        "addAccounts": True,
                        "updateAccountContent": False,
                        "updateAccountProperties": False,
                        "initiateCPMAccountManagementOperations": False,
                        "specifyNextAccountContent": False,
                        "renameAccounts": False,
                        "deleteAccounts": False,
                        "unlockAccounts": False,
                        "manageSafe": False,
                        "manageSafeMembers": False,
                        "backupSafe": False,
                        "viewAuditLog": False,
                        "viewSafeMembers": False,
                        "accessWithoutConfirmation": False,
                        "createFolders": False,
                        "deleteFolders": False,
                        "moveAccountsAndFolders": False,
                        "requestsAuthorizationLevel1": False,
                        "requestsAuthorizationLevel2": False
                    },
                    "MemberType": "Group"
                }
            )
        except CustomException as e:
            if e.status == 409:
                pass # re-use existing members.
            else:
                raise e
        except Exception as e:
            raise e



    def __addCyberArkAccounts(self, asset: dict) -> list:
        o = list()

        try:
            for account in self.params["accounts"]:
                Log.actionLog(
                    f"[USE CASE] Creating Account {account['name']} and adding to Safe {self.params['safe']['name']}")

                createdAccountInformation = Safe(asset=asset, id=self.params["safe"]["name"], sessionUid=self.sessionUid).addAccount(data={
                    "platformId": account["platform"],
                    "safeName": self.params["safe"]["name"],
                    "name": account["name"],
                    "address": account["address"],
                    "userName": account["userName"],
                    "secretType": "password",
                    "secret": account["secret"],
                    "platformAccountProperties": {
                        "Encoded": "Yes" if account.get("encoded", False) else "No",
                        "Key": account["key"],
                        "Mapping": "|"
                    }
                })

                o.append({
                    "userName": account["userName"],
                    "uuid": f"{createdAccountInformation.get('id')}@{createdAccountInformation.get('createdTime')}"
                })

            return o
        except Exception as e:
            raise e



    def __findSlot(self, asset: dict, accountInformation: dict) -> int:
        try:
            # Fetch all accounts with the same Key value as accountInformation (in the same Safe).
            highestMatch = 0
            slots = list()

            accountKey = accountInformation.get("platformAccountProperties", {}).get("Key", "")
            accountsWithSameKey = Account.rawDataList(asset, self.params["safe"]["name"], noCache=True, userFilters=[
                "platformAccountProperties.Key eq " + accountKey
            ], sessionUid=self.sessionUid)

            # Find accounts belonging to the input application and extract the highest unused slot.
            for awk in accountsWithSameKey:
                m = awk.get("platformAccountProperties", {}).get("Mapping", "")
                if f"|{self.params['app']['name']}@" in m:
                    matches = re.search(r"(?<=@)(\d)(?=|)", m) # example: 1 for |pba2-be@1|.
                    if matches:
                        match = int(matches.group(1))
                        slots.append(match)

            # Extract the highest unused slot.
            slots.sort() # example: [1, 2, 3, 6, 7] -> 4 needed.

            for j in range(len(slots) - 1):
                if slots[j + 1] > slots[j] + 1:
                    highestMatch = slots[j] + 1
                    break
            if not highestMatch:
                highestMatch = len(slots) + 1
        except Exception as e:
            raise e

        return highestMatch



    def __manageForcedSlot(self, asset: dict, userAccount: dict) -> int:
        try:
            slot = int(userAccount["slot"])
            if slot:
                # If slot il already taken by another account within the same Safe,
                # clear ye olde mapping (force True) or raise an error otherwise.
                allAccounts = Account.rawDataList(asset, self.params["safe"]["name"], sessionUid=self.sessionUid)
                for a in allAccounts:
                    mapping = a.get("platformAccountProperties", {}).get("Mapping", "")
                    if f"|{self.params['app']['name']}@{slot}|" in mapping:
                        if bool(userAccount["force"]):
                            Log.actionLog(f"[USE CASE] Replacing {a['id']} in slot {slot} with {userAccount['uuid']}...")

                            Account(asset=asset, id=a["id"], sessionUid=self.sessionUid).modify(data={
                                "platformAccountProperties": {
                                    "Mapping": mapping.replace(f"|{self.params['app']['name']}@{slot}|", "|")
                                }
                            })
                        else:
                            raise CustomException(status=409, payload={"Backend": "[ERROR] Slot " + str(slot) + " is already in use. Unprocessed account: " + userAccount["uuid"]})

                        break
            else:
                raise CustomException(status=409, payload={"Backend": "[ERROR] Incorrect slot " + str(slot) + " for account: " + userAccount["uuid"]})
        except Exception as e:
            raise e

        return slot



    def __modifyCyberArkAccounts(self, asset: dict) -> list:
        result = []

        try:
            for account in self.params["accounts"]:
                Log.actionLog(
                    f"[USE CASE] Modifying Account {account['uuid']}")

                # Fetch the account corresponding to id and createdTime taken from account["uuid"] input (id@timestamp), for the input safe.
                paramsList = account.get("uuid", "").split("@")
                try:
                    accountInformation = Account.rawDataList(asset, self.params["safe"]["name"], userFilters=[ # @todo: direct filter via API.
                        "id eq " + paramsList[0],
                        "createdTime eq " + paramsList[1]
                    ], sessionUid=self.sessionUid)[0]
                except IndexError:
                    raise CustomException(status=404)

                # Update Mapping meta information and persist (modify account), if account not already associated with the application.
                accountMapping = accountInformation.get("platformAccountProperties", {}).get("Mapping", "")
                if f"|{self.params['app']['name']}@" not in accountMapping:
                    if account["slot"] == "auto":
                        slot = self.__findSlot(asset, accountInformation)
                    else:
                        slot = self.__manageForcedSlot(asset, account)

                    newMapping = f"|{self.params['app']['name']}@{slot}|"
                    if newMapping not in accountMapping:
                        accountMapping += newMapping[1:]

                    Account(asset=asset, id=accountInformation["id"], sessionUid=self.sessionUid).modify(data={
                        "platformAccountProperties": {
                            "Mapping": accountMapping
                        }
                    })

                    result.append({
                        "account": account.get("uuid", ""),
                        "app": {
                            "name": self.params['app']['name'],
                            "namespace": self.params['app']['namespace']
                        },
                        "slot": slot
                    })
        except IndexError:
            raise CustomException(status=400)
        except Exception as e:
            raise e

        return result



    ####################################################################################################################
    # Private methods, Kubernetes
    ####################################################################################################################

    def __saveK8sConfigFiles(self, accountsMappedToTheApplication: list, path: str) -> None:
        Log.actionLog(f"[USE CASE] Generating Kubernetes resources")

        k8sFiles = [
            ("conjur-external-secret-standard.yaml", "externalSecretStandard"),
            ("namespace.yml", "namespace")
        ]

        accountsType = {
            "standard": [],
            "encoded": []
        }

        try:
            for account in accountsMappedToTheApplication:
                if account["platformAccountProperties"].get("Encoded") == "Yes":
                    accountsType["encoded"].append(account)
                else:
                    accountsType["standard"].append(account)

            # External secrets, standard accounts.
            content = {
                "apiVersion": "external-secrets.io/v1beta1",
                "kind": "ExternalSecret",
                "metadata": {
                    "name": f"{self.params['app']['name']}-environment-ops",
                    "namespace": self.params["app"]["namespace"]
                },
                "spec": {
                    "refreshInterval": "10s",
                    "secretStoreRef": {
                        "name": "conjur",
                        "kind": "ClusterSecretStore"
                    },
                    "data": []
                }
            }
            for standardAccount in accountsType["standard"]:
                slot = BPER.__accountSlot(standardAccount)
                if slot:
                    content["spec"]["data"].append(
                        {
                            "secretKey": standardAccount.get("platformAccountProperties", {}).get("Key") + "_" + str(slot),
                            "userName": standardAccount.get("userName", ""),
                            "remoteRef": {
                                "key": f"{self.params['vault']['name']}/{self.params['safe']['member']}/{self.params['safe']['name']}/{standardAccount['name']}/password",
                                "decodingStrategy": "None"
                            }
                        }
                    )
                else:
                    raise CustomException(status=400, payload={"Backend": "Missing slot in account"})

            externalSecretStandard = yaml.dump(content).replace("userName", "#userName")

            # External secrets, encoded (base 64) accounts.
            if len(accountsType["encoded"]) > 0:
                k8sFiles.append(
                    ("conjur-external-secret-encoded.yaml", "externalSecretEncoded")
                )

                content = {
                    "apiVersion": "external-secrets.io/v1beta1",
                    "kind": "ExternalSecret",
                    "metadata": {
                        "name": f"{self.params['app']['name']}-ops",
                        "namespace": self.params["app"]["namespace"]
                    },
                    "spec": {
                        "refreshInterval": "10s",
                        "secretStoreRef": {
                            "name": "conjur",
                            "kind": "ClusterSecretStore"
                        },
                        "data": []
                    }
                }
                for encodedAccount in accountsType["encoded"]:
                    slot = BPER.__accountSlot(encodedAccount)
                    if slot:
                        content["spec"]["data"].append(
                            {
                                "secretKey": encodedAccount.get("platformAccountProperties", {}).get("Key") + "_" + str(slot),
                                "userName": encodedAccount.get("userName", ""),
                                "remoteRef": {
                                    "key": f"{self.params['vault']['name']}/{self.params['safe']['member']}/{self.params['safe']['name']}/{encodedAccount['name']}/password",
                                    "decodingStrategy": "Base64"
                                }
                            }
                        )
                    else:
                        raise CustomException(status=400, payload={"Backend": "Missing slot in account"})

                externalSecretEncoded = yaml.dump(content).replace("userName", "#userName")

            # Namespace.
            namespace = yaml.dump({
                "apiVersion": "v1",
                "kind": "Namespace",
                "metadata": {
                    "name": self.params["app"]["namespace"],
                    "labels": {
                        "name": self.params["app"]["name"]
                    }
                }
            })

            for configFile in k8sFiles:
                Log.actionLog(f"[USE CASE] File: {configFile[0]}\r\n + {eval(configFile[1])}")

                # @todo: overwrite the actual files or add/replace content?

                with open(f"{path}/{configFile[0]}", mode="w") as f:
                    f.write(eval(configFile[1]))
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private static methods
    ####################################################################################################################

    @staticmethod
    def __validate(what: list) -> None:
        try:
            for w in what:
                data: dict = w[0]
                criterium: str = w[1]

                if criterium == "no-uppercase":
                    for k, v in data.items():
                        if re.search(r"[A-Z]", v):
                            raise CustomException(status=400, payload={"Backend": "Uppercase letters not allowed in app data"})

                if criterium == "no-at-pipe":
                    for k, v in data.items():
                        if re.search(r"@", v):
                            raise CustomException(status=400, payload={"Backend": "@ letter not allowed in app data"})
                        if re.search(r"\|", v):
                            raise CustomException(status=400, payload={"Backend": "| letter not allowed in app data"})
        except Exception as e:
            raise e



    @staticmethod
    def __accountSlot(account: dict) -> int:
        slot = 0

        try:
            matches = re.search(r"(?<=@)(\d)(?=|)", account.get("platformAccountProperties", {}).get("Mapping", ""))
            if matches:
                slot = int(matches.group(1))
        except Exception as e:
            raise e

        return slot
