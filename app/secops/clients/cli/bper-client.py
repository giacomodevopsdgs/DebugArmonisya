#!/usr/bin/python3
import re
import json

import django
import argparse
from django.test import Client

import init
from helpers import *

#
import os
print("📍 Running:", os.path.realpath(__file__))

########################################################################################################################
# CyberArk
########################################################################################################################

class CyberArk:
    @staticmethod
    @errorHandler
    def safes(config: dict) -> dict:
        try:
            return Client().get(
                path="/api/v1/secops/cyberark/safes/",
                headers=CyberArk.__headers(config),
                query_params={}
            )
        except Exception as e:
            raise e



    @staticmethod
    @errorHandler
    def safeAccounts(config: dict, safeIdentifier: str) -> dict:
        try:
            return Client().get(
                path=f"/api/v1/secops/cyberark/safe/{safeIdentifier}/accounts/",
                headers=CyberArk.__headers(config),
                query_params={}
            )
        except Exception as e:
            raise e



    @staticmethod
    def __headers(config: dict):
        return {
            "CyberArk-TLS-Verify": config.get("tlsVerify", True),
            "CyberArk-BaseURL": config.get("baseurl", ""),
            "CyberArk-Username": config.get("username", ""),

            "CyberArkCCP-Baseurl": config.get("ccpBaseurl", ""),
            "CyberArkCCP-AppId": config.get("ccpAppId", ""),
            "CyberArkCCP-Username": config.get("ccpUsername", "")
        }



########################################################################################################################
# BPER use case
########################################################################################################################

class BPER:
    @staticmethod
    @errorHandler
    def cyberarkInsert(config: dict, data: dict) -> dict:
        try:
            return Client().post(
                path="/api/v1/secops/usecases/bper/cyberark-insert/",
                headers=BPER.__headers(config),
                content_type="application/json",
                query_params={},
                data=data
            )
        except Exception as e:
            raise e



    @staticmethod
    @errorHandler
    def cyberarkModify(config: dict, data: dict) -> dict:
        try:
            return Client().post(
                path="/api/v1/secops/usecases/bper/cyberark-modify/",
                headers=BPER.__headers(config),
                content_type="application/json",
                query_params={},
                data=data
            )
        except Exception as e:
            raise e



    @staticmethod
    def __headers(config: dict):
        return {
            "CyberArk-TLS-Verify": config["CYBERARK"].get("tlsVerify", True),
            "CyberArk-BaseURL": config["CYBERARK"].get("baseurl", ""),
            "CyberArk-Username": config["CYBERARK"].get("username", ""),

            "CyberArkCCP-Baseurl": config["CYBERARK"].get("ccpBaseurl", ""),
            "CyberArkCCP-AppId": config["CYBERARK"].get("ccpAppId", ""),
            "CyberArkCCP-Username": config["CYBERARK"].get("ccpUsername", ""),

            "Git-BaseURL": config["GIT"].get("remote", ""),
            "Git-RepoKey": config["GIT"].get("repoKey", ""),
            "Git-UserKeyBase64": config["GIT"].get("userKeyBase64", "")
        }



########################################################################################################################
# Main
########################################################################################################################

userInput = dict()

try:
    CYBERARK = {}
    from config import *
except ModuleNotFoundError:
    pass

try:
    django.setup()

    # Handle user input.
    parser = argparse.ArgumentParser()
    parser.add_argument('--cyberark', nargs='?', help='Manage CyberArk endpoint', required=False)
    parser.add_argument('--action', help='insert/associate', required=False)

    parser.add_argument('--vaultName', help='', required=False)
    parser.add_argument('--safeName', help='', required=False)
    parser.add_argument('--safeDescription', help='', required=False)
    parser.add_argument('--safeMember', help='', required=False)
    parser.add_argument('--accountsDescriptionJsonFile', help='', required=False)
    parser.add_argument('--appName', help='', required=False)
    parser.add_argument('--appNamespace', help='', required=False)
    parser.add_argument('--ticket', help='', required=False)
    args = parser.parse_args()

    for j in ("vaultName", "safeName", "safeDescription", "safeMember", "accountsDescriptionJsonFile", "appName", "appNamespace", "ticket"):
        if getattr(args, j):
            userInput[j] = getattr(args, j)

    if "safeDescription" not in userInput:
        userInput["safeDescription"] = ""

    if userInput.get("accountsDescriptionJsonFile"):
        with open(userInput["accountsDescriptionJsonFile"]) as f:
            userInput["accounts"] = json.loads(f.read().replace("\n", "").replace("\r", ""))

    # Models.
    if args.cyberark:
        argValue = args.cyberark.replace("\"", "")

        # --cyberark "safe=SAFE_ID accounts".
        if re.match(r"^safe\s*=\s*.*\s*accounts$", argValue):
            safeId = ""
            m = re.search(r"safe\s*=\s*(\S+)\s*.*", argValue) # SAFE_ID.
            if m:
                safeId = m.group(1)
                if safeId:
                    Util.log(CyberArk.safeAccounts(config=CYBERARK, safeIdentifier=safeId))

        # --cyberark "safes list".
        if args.cyberark == "safes list":
            Util.log(CyberArk.safes(config=CYBERARK))

    # Use cases.
    if args.action:
        if args.action == "insert":
            # Check user input for required data.
            for j in ("safeName", "safeMember", "accounts"):
                if j not in userInput:
                    raise Exception("Missing value for: " + j)

            Util.log(BPER.cyberarkInsert(
                config={
                    "CYBERARK": CYBERARK,
                    "GIT": GIT
                },
                data={
                    "data": {
                        "safe": {
                            "name": userInput["safeName"],
                            "description": userInput["safeDescription"],
                            "member": userInput["safeMember"]
                        },
                        "accounts": userInput["accounts"]
                    }
                }
            ))

        if args.action == "associate":
            # Check user input for required data.
            for j in ("vaultName", "safeName", "safeMember", "accounts", "appName", "appNamespace", "ticket"):
                if j not in userInput:
                    raise Exception("Missing value for: " + j)

            Util.log(BPER.cyberarkModify(
                config={
                    "CYBERARK": CYBERARK,
                    "GIT": GIT
                },
                data={
                    "data": {
                        "vault": {
                            "name": userInput["vaultName"]
                        },
                        "safe": {
                            "name": userInput["safeName"],
                            "member": userInput["safeMember"]
                        },
                        "accounts": userInput["accounts"],
                        "app": {
                            "name": userInput["appName"],
                            "namespace": userInput["appNamespace"]
                        },
                        "ticket": userInput["ticket"]
                    }
                }
            ))
except Exception as ex:
    raise ex

    Util.out(ex.__str__())
    exit(1)
