import base64
from typing import Callable

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from secops.models.Asset.Asset import Asset
from secops.models.Permission.Permission import Permission
from secops.models.CyberArk.Session.Session import Session as CyberArkSession
from secops.models.Conjur.Session.Session import Session as ConjurArkSession

from secops.controllers.CustomControllerBase import CustomControllerBase

from secops.helpers.Lock import Lock
from secops.helpers.Conditional import Conditional
from secops.helpers.decorators.ActionHistory import historyLog
from secops.helpers.Log import Log


class CustomController(CustomControllerBase):
    def __init__(self, subject: str, *args, **kwargs):
        self.subject = subject



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    @historyLog
    def info(self, request: Request, objectUid: str, actionCall: Callable, technology: list = None, Serializer=None, doLock: bool = True) -> Response:
        data = dict()
        technology = technology or []
        sessionUid = self.generateSessionUid()
        etagCondition = {"responseEtag": ""}

        action = self.subject + "_get"
        actionLog = f"Information for {self.subject.capitalize()} {objectUid}"
        lockedObjectClass = self.subject

        asset = CustomController.__assets(request, technology)[technology[0]]

        try:
            user = self.loggedUser(request)
            if Permission.hasUserPermission(groups=user["groups"], action=action) or user["authDisabled"]:
                Log.actionLog(actionLog, user)

                lock = Lock(lockedObjectClass, locals(), objectUid, doLock=doLock)
                if lock.isUnlocked():
                    lock.lock()

                    data = {
                        "data":
                            self.validate(
                                actionCall(
                                    sessionUid=sessionUid,
                                    asset=asset,
                                    id=objectUid
                                ),
                                Serializer,
                                "value"
                            ),
                        "href": request.get_full_path()
                    }

                    # Check the response's ETag validity (against client request).
                    conditional = Conditional(request)
                    etagCondition = conditional.responseEtagFreshnessAgainstRequest(data["data"])
                    if etagCondition["state"] == "fresh":
                        data = None
                        httpStatus = status.HTTP_304_NOT_MODIFIED
                    else:
                        httpStatus = status.HTTP_200_OK

                    lock.release()
                else:
                    data = None
                    httpStatus = status.HTTP_423_LOCKED
            else:
                data = None
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            Lock(lockedObjectClass, locals(), objectUid).release()

            data, httpStatus, headers = self.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)
        finally:
            if "cyberark" in technology:
                CyberArkSession.delete(sessionUid, asset)
            if "conjur" in technology:
                ConjurArkSession.delete(sessionUid, asset)

        return Response(data, status=httpStatus, headers={
            "ETag": etagCondition["responseEtag"],
            "Cache-Control": "must-revalidate"
        })



    @historyLog
    def ls(self, request: Request, actionCall: Callable, technology: list = None, parentId: str = "", Serializer=None, openCall: bool = False, doLock: bool = True) -> Response:
        data = dict()
        technology = technology or []
        sessionUid = self.generateSessionUid()
        etagCondition = {"responseEtag": ""}

        if parentId:
            # Example: list of safe's accounts.
            action = self.subject + "_get"
            actionLog = f"Information for {self.subject.capitalize()} {parentId}"
        else:
            if self.subject[-1:] == "y":
                action = self.subject[:-1] + "ies_get" # example: categories_get.
            else:
                action = self.subject + "s_get" # example: users_get.
            actionLog = f"List of {self.subject.capitalize()}"

        lockedObjectClass = self.subject

        asset = CustomController.__assets(request, technology).get(technology[0])

        try:
            user = self.loggedUser(request)
            if Permission.hasUserPermission(groups=user["groups"], action=action) or user["authDisabled"] or openCall:
                Log.actionLog(actionLog, user)

                lock = Lock(lockedObjectClass, locals(), doLock=doLock)
                if lock.isUnlocked():
                    lock.lock()

                    data = {
                        "data": {
                            "items": self.validate(
                                actionCall(
                                    sessionUid=sessionUid,
                                    asset=asset,
                                    parentId=parentId
                                ),
                                Serializer,
                                "list"
                            )
                        },
                        "href": request.get_full_path()
                    }

                    # Check the response's ETag validity (against client request).
                    conditional = Conditional(request)
                    etagCondition = conditional.responseEtagFreshnessAgainstRequest(data["data"])
                    if etagCondition["state"] == "fresh":
                        data = None
                        httpStatus = status.HTTP_304_NOT_MODIFIED
                    else:
                        httpStatus = status.HTTP_200_OK

                    lock.release()
                else:
                    data = None
                    httpStatus = status.HTTP_423_LOCKED
            else:
                data = None
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            Lock(lockedObjectClass, locals()).release()

            data, httpStatus, headers = self.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)
        finally:
            if "cyberark" in technology:
                CyberArkSession.delete(sessionUid, asset)
            if "conjur" in technology:
                ConjurArkSession.delete(sessionUid, asset)

        return Response(data, status=httpStatus, headers={
            "ETag": etagCondition["responseEtag"],
            "Cache-Control": "must-revalidate"
        })



    @historyLog
    def add(self, request: Request, actionCall: Callable, technology: list = None, parentId: str = "", Serializer=None, doLock: bool = True) -> Response:
        data = None
        technology = technology or []
        sessionUid = self.generateSessionUid()

        if parentId:
            action = self.subject + "_post"
            actionLog = f"Item modification for {self.subject.capitalize()} {parentId}"
        else:
            action = self.subject + "_post"
            actionLog = f"Item addition for {self.subject.capitalize()}"

        lockedObjectClass = self.subject

        asset = CustomController.__assets(request, technology)[technology[0]]

        try:
            user = self.loggedUser(request)
            if Permission.hasUserPermission(groups=user["groups"], action=action) or user["authDisabled"]:
                Log.actionLog(actionLog, user)

                lock = Lock(lockedObjectClass, locals(), doLock=doLock)
                if lock.isUnlocked():
                    lock.lock()

                    if isinstance(request.data, dict):
                        inputData = request.data.get("data", {})
                    else:
                        inputData = request.data

                    self.validate(inputData, Serializer, "value")

                    o = actionCall(
                        sessionUid=sessionUid,
                        asset=asset,
                        parentId=parentId,
                        data=inputData
                    )

                    if o:
                        data = {
                            "data": o
                        }

                    httpStatus = status.HTTP_201_CREATED

                    lock.release()
                else:
                    data = None
                    httpStatus = status.HTTP_423_LOCKED
            else:
                data = None
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            Lock(lockedObjectClass, locals()).release()

            data, httpStatus, headers = self.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)
        finally:
            if "cyberark" in technology:
                CyberArkSession.delete(sessionUid, asset)
            if "conjur" in technology:
                ConjurArkSession.delete(sessionUid, asset)

        return Response(data, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })



    @historyLog
    def run(self, request: Request, actionCall: Callable, technology: list = None, Serializer=None, doLock: bool = True) -> Response:
        data = None
        technology = technology or []
        sessionUid = self.generateSessionUid()

        action = self.subject + "_run"
        actionLog = f"Running {self.subject.capitalize()}"

        lockedObjectClass = self.subject

        assets = CustomController.__assets(request, technology)

        try:
            user = self.loggedUser(request)
            if Permission.hasUserPermission(groups=user["groups"], action=action) or user["authDisabled"]:
                Log.actionLog(actionLog, user)

                lock = Lock(lockedObjectClass, locals(), doLock=doLock)
                if lock.isUnlocked():
                    lock.lock()

                    self.validate(
                        request.data.get("data", {}),
                        Serializer,
                        "value"
                    )

                    o = actionCall(
                        sessionUid=sessionUid,
                        assets=assets,
                        data=request.data.get("data", {})
                    )

                    if o:
                        data = {
                            "data": o
                        }

                    httpStatus = status.HTTP_200_OK

                    lock.release()
                else:
                    data = None
                    httpStatus = status.HTTP_423_LOCKED
            else:
                data = None
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            Lock(lockedObjectClass, locals()).release()

            data, httpStatus, headers = self.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)
        finally:
            if "cyberark" in technology:
                ConjurArkSession.delete(sessionUid, assets["cyberark"])
            if "conjur" in technology:
                ConjurArkSession.delete(sessionUid, assets["conjur"])

        return Response(data, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })



    @historyLog
    def modify(self, request: Request, objectUid: str, actionCall: Callable, technology: list = None, Serializer=None, doLock: bool = True) -> Response:
        data = None
        technology = technology or []
        sessionUid = self.generateSessionUid()
        action = self.subject + "_patch"
        actionLog = f"Item modification for {self.subject.capitalize()}"
        lockedObjectClass = self.subject

        asset = CustomController.__assets(request, technology)[technology[0]]

        try:
            user = self.loggedUser(request)
            if Permission.hasUserPermission(groups=user["groups"], action=action) or user["authDisabled"]:
                Log.actionLog(actionLog, user)

                lock = Lock(lockedObjectClass, locals(), objectUid, doLock=doLock)
                if lock.isUnlocked():
                    lock.lock()

                    self.validate(
                        request.data.get("data", {}),
                        Serializer,
                        "value",
                        partial=True
                    )

                    o = actionCall(
                        sessionUid=sessionUid,
                        asset=asset,
                        id=objectUid,
                        data=request.data.get("data", {})
                    )

                    if o:
                        data = {
                            "data": o
                        }

                    httpStatus = status.HTTP_200_OK

                    lock.release()
                else:
                    data = None
                    httpStatus = status.HTTP_423_LOCKED
            else:
                data = None
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            Lock(lockedObjectClass, locals(), objectUid).release()

            data, httpStatus, headers = self.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)
        finally:
            if "cyberark" in technology:
                CyberArkSession.delete(sessionUid, asset)
            if "conjur" in technology:
                ConjurArkSession.delete(sessionUid, asset)

        return Response(data, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })



    @historyLog
    def remove(self, request: Request, objectUid: str, actionCall: Callable, technology: list = None, doLock: bool = True) -> Response:
        data = None
        technology = technology or []
        sessionUid = self.generateSessionUid()
        action = self.subject + "_delete"
        actionLog = f"Item deletion for {self.subject.capitalize()}"
        lockedObjectClass = self.subject

        asset = CustomController.__assets(request, technology)[technology[0]]

        try:
            user = self.loggedUser(request)
            if Permission.hasUserPermission(groups=user["groups"], action=action) or user["authDisabled"]:
                Log.actionLog(actionLog, user)

                lock = Lock(lockedObjectClass, locals(), objectUid, doLock=doLock)
                if lock.isUnlocked():
                    lock.lock()

                    o = actionCall(
                        sessionUid=sessionUid,
                        asset=asset,
                        id=objectUid
                    )

                    if o:
                        data = {
                            "data": o
                        }

                    httpStatus = status.HTTP_200_OK

                    lock.release()
                else:
                    data = None
                    httpStatus = status.HTTP_423_LOCKED
            else:
                data = None
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            Lock(lockedObjectClass, locals(), objectUid).release()

            data, httpStatus, headers = self.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)
        finally:
            if "cyberark" in technology:
                CyberArkSession.delete(sessionUid, asset)
            if "conjur" in technology:
                ConjurArkSession.delete(sessionUid, asset)

        return Response(data, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })



    ####################################################################################################################
    # Private static methods
    ####################################################################################################################

    @staticmethod
    def __assets(request: Request, technology: list) -> dict:
        assets = dict()

        try:
            # If asset information passed by the user, use this instead of fetching from db.
            if request.headers.get("CyberArk-BaseURL") or request.headers.get("Git-BaseURL"):
                if request.headers.get("CyberArk-BaseURL", ""):
                    assets["cyberark"] = {
                        "technology": "cyberark",
                        "tlsverify": bool(int(request.headers.get("CyberArk-TLS-Verify", 1))),
                        "baseurl": request.headers.get("CyberArk-BaseURL", ""),
                        "username": request.headers.get("CyberArk-Username", ""),

                        "ccpBaseurl": request.headers.get("CyberArkCCP-Baseurl", ""),
                        "appId": request.headers.get("CyberArkCCP-AppId", ""),
                        "ccpUsername": request.headers.get("CyberArkCCP-Username", "")
                    }
                # @todo: conjur.
                # @todo: kubernetes.
                if request.headers.get("Git-BaseURL", ""):
                    assets["git"] = {
                        "technology": "git",
                        "baseurl": request.headers.get("Git-BaseURL", ""), # remote.
                        "repokey": request.headers.get("Git-RepoKey", ""),
                        "userkey": base64.b64decode(
                            request.headers.get("Git-UserKeyBase64", "")
                        ).decode("utf-8")
                    }
            else:
                if technology:
                    if "cyberark" in technology:
                        cyberArkAsset = Asset.getAssetIdOfTechnology("cyberark")
                        cyberArkCCPAsset = Asset.getAssetIdOfTechnology("cyberark-ccp")

                        assets["cyberark"] = {
                            "technology": "cyberark",
                            "tlsverify":  bool(int(cyberArkAsset.get("tlsverify", 1))),
                            "baseurl": cyberArkAsset.get("baseurl", ""),
                            "username": cyberArkAsset.get("username", ""),

                            "ccpBaseurl": cyberArkCCPAsset.get("baseurl", ""),
                            "appId": cyberArkCCPAsset.get("appid", ""),
                            "ccpUsername": cyberArkCCPAsset.get("username", "")
                        }
                    if "conjur" in technology:
                        cyberArkAsset = Asset.getAssetIdOfTechnology("conjur")
                        assets["conjur"] = {
                            "technology": "conjur",
                            "tlsverify":  bool(int(cyberArkAsset.get("tlsverify", 1))),
                            "baseurl": cyberArkAsset.get("baseurl", ""),
                            "username": cyberArkAsset.get("username", ""),
                            "password": cyberArkAsset.get("password", ""),
                            "account": cyberArkAsset.get("account", "")
                        }
                    if "kubernetes" in technology:
                        cyberArkAsset = Asset.getAssetIdOfTechnology("kubernetes")
                        assets["kubernetes"] = {
                            "technology": "kubernetes",
                            "baseurl": cyberArkAsset.get("baseurl", ""),
                            "certificateAuthorityData": cyberArkAsset.get("certificate_authority_data", ""),
                            "clientCertificateData": cyberArkAsset.get("client_certificate_data", ""),
                            "clientKeyData": cyberArkAsset.get("client_key_data", "")
                        }
                    if "git" in technology:
                        gitAsset = Asset.getAssetIdOfTechnology("git")
                        assets["git"] = {
                            "technology": "git",
                            "baseurl":  gitAsset.get("baseurl", ""),
                            "repokey": gitAsset.get("repokey", ""),
                            "userkey": gitAsset.get("userkey", "")
                        }
                else:
                    pass # no need for asset information.
        except Exception as e:
            raise e

        return assets
