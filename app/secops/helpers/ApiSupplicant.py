import json
import time
import re
import requests
from typing import Callable, Union, Dict, List

from django.conf import settings

from secops.models.CyberArk.Session.Session import Session as CyberArkSession
from secops.models.Conjur.Session.Session import Session as ConjurSession

from secops.helpers.Log import Log
from secops.helpers.Exception import CustomException


class ApiSupplicant:
    def __init__(self, endpoint: str, asset: dict, accessType: str, certificates: tuple = None, headers: dict = None, params: dict = None, data: Union[Dict, List, str] = None, jsonPayload: bool = True,
            silent: bool = False, sessionUid: str = "", handlingSession: bool = False, **kwargs
        ):
        self.httpProxy = settings.API_SUPPLICANT_HTTP_PROXY

        self.handlingSession = handlingSession
        self.silent = silent

        self.accessType = accessType
        self.sessionUid = sessionUid
        self.asset = asset
        self.certificates = certificates or ()
        self.headers = headers or {}
        self.params = params or {}
        self.data = data or None
        self.jsonPayload = jsonPayload

        if accessType in ("cyberark", "conjur"):
            self.url = self.asset.get("baseurl", "//") + endpoint
        elif accessType == "cyberark-ccp":
            self.url = self.asset.get("ccpBaseurl", "//") + endpoint
        else:
            self.url = "//"



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def get(self) -> dict:
        try:
            Log.actionLog("[API Supplicant] Fetching remote: GET " + str(self.url)+" with params: " + str(self.params))
            return self.__request(request=requests.get)
        except Exception as e:
            raise e



    def post(self) -> dict:
        try:
            Log.actionLog("[API Supplicant] Posting to remote: " + str(self.url))
            if not self.silent:
                Log.actionLog("[API Supplicant] Posting data: " + str(self.data))

            return self.__request(request=requests.post)
        except Exception as e:
            raise e



    def put(self) -> dict:
        try:
            Log.actionLog("[API Supplicant] Putting to remote: " + str(self.url))
            return self.__request(request=requests.put)
        except Exception as e:
            raise e



    def patch(self) -> dict:
        try:
            Log.actionLog("[API Supplicant] Patching remote: " + str(self.url))
            return self.__request(request=requests.patch)
        except Exception as e:
            raise e



    def delete(self) -> dict:
        try:
            Log.actionLog("[API Supplicant] Deleting remote: " + str(self.url))
            return self.__request(request=requests.delete)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __request(self, request: Callable) -> dict:
        # In the event of a network problem (e.g. DNS failure, refused connection, etc), Requests will raise a ConnectionError exception.
        # If a request times out, a Timeout exception is raised.
        # If a request exceeds the configured number of maximum redirections, a TooManyRedirects exception is raised.
        # SSLError on SSL/TLS error.
        # On KO status codes, a CustomException is raised, with response status and body.

        try:
            if self.jsonPayload:
                headers = {
                    "Content-Type": "application/json"
                }
            else:
                headers = {
                    "Content-Type": "text/plain"
                }

            headers.update(self.headers)

            # Non-handling session calls, retrieve access token.
            if not self.handlingSession:
                if self.accessType == "cyberark":
                    headers.update({
                        "Authorization": CyberArkSession.getCyberArkSessionToken(self.sessionUid, self.asset)
                    })
                if self.accessType == "conjur":
                    headers.update({
                        "Authorization": ConjurSession.getConjurSessionToken(self.sessionUid, self.asset)
                    })

            Log.actionLog(
                "[API Supplicant] Request headers: " + str(headers))

            response = request(
                verify=self.asset.get("tlsverify", True),
                cert=self.certificates,
                proxies=self.httpProxy,
                timeout=settings.API_SUPPLICANT_NETWORK_TIMEOUT,
                url=self.url,
                headers=headers,
                params=self.params, # GET parameters.
                data=json.dumps(self.data) if self.jsonPayload else self.data, # POST parameters.
                stream=True
            )

            try:
                responsePayload = response.json()
            except requests.exceptions.JSONDecodeError:
                responsePayload = response.text
            except Exception:
                responsePayload = {}

            if not self.silent:
                for j in (("status", response.status_code), ("headers", response.headers), ("payload", responsePayload)):
                    Log.actionLog("[API Supplicant] Remote response " + j[0] + ": " + str(j[1]))

            # CustomException errors on connection ok but ko status code.
            if response.status_code in (200, 201, 202, 204, 206):
                pass
            elif response.status_code in (401, 403):
                if self.accessType == "cyberark":
                    CyberArkSession.delete(self.sessionUid, self.asset) # delete possibly expired session data.

                    raise CustomException(status=400, payload={
                        "Remote": {
                            "error": "Wrong credentials for the asset or remote token expired",
                            "code": response.status_code,
                            "reason": responsePayload.get("ErrorMessage", "unknown")
                        }
                    })
                if self.accessType == "conjur":
                    ConjurSession.delete(self.sessionUid, self.asset) # delete possibly expired session data.

                    raise CustomException(status=400, payload={
                        "Remote": {
                            "error": "Wrong credentials for the asset or remote token expired",
                            "code": response.status_code
                        }
                    })
            elif response.status_code == 429:
                if "Retry-After" in responsePayload and re.search(" seconds$", responsePayload["Retry-After"]):
                    Log.actionLog("[API Supplicant] Waiting after a Too many request message")
                    time.sleep(
                        int(re.sub(" seconds", "", responsePayload["Retry-After"]))
                    )
                    self.__request(request=request)
                else:
                    raise CustomException(status=response.status_code, payload={"Remote": responsePayload})
            else:
                raise CustomException(status=response.status_code, payload={"Remote": responsePayload})
        except Exception as e:
            raise e

        time.sleep(0.2) # try avoiding throttle limits.

        return {
            "headers": response.headers,
            "payload": responsePayload,
            "status": response.status_code
        }
