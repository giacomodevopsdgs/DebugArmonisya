from rest_framework.request import Request
from rest_framework.response import Response

from secops.controllers.CustomController import CustomController

from secops.models.CyberArk.Account import Account


class AccountController(CustomController):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="cyberark_account", *args, **kwargs)



    def get(self, request: Request, id: str) -> Response:
        def actionCall(**kwargs):
            return Account(**kwargs).repr()

        return self.info(
            technology=["cyberark"],
            request=request,
            actionCall=actionCall,
            objectUid=id,
            doLock=False
        )



    def delete(self, request: Request, id: str) -> Response:
        def actionCall(**kwargs):
            return Account(**kwargs).delete()

        return self.remove(
            technology=["cyberark"],
            request=request,
            actionCall=actionCall,
            objectUid=id,
            doLock=False
        )



    def patch(self, request: Request, id: str) -> Response:
        def actionCall(**kwargs):
            return Account(kwargs["asset"], kwargs["id"]).modify(data=kwargs["data"])

        return self.modify(
            technology=["cyberark"],
            request=request,
            actionCall=actionCall,
            objectUid=id,
            doLock=False
        )
