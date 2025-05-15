from rest_framework.request import Request
from rest_framework.response import Response

from secops.controllers.CustomController import CustomController

from secops.models.CyberArk.Safe import Safe


class SafeController(CustomController):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="cyberark_safe", *args, **kwargs)



    def get(self, request: Request, id: str) -> Response:
        def actionCall(**kwargs):
            return Safe(**kwargs).repr()

        return self.info(
            technology=["cyberark"],
            request=request,
            actionCall=actionCall,
            objectUid=id,
            doLock=False
        )



    def delete(self, request: Request, id: str) -> Response:
        def actionCall(**kwargs):
            return Safe(**kwargs).delete()

        return self.remove(
            technology=["cyberark"],
            request=request,
            actionCall=actionCall,
            objectUid=id,
            doLock=False
        )



    def patch(self, request: Request, id: str) -> Response:
        def actionCall(**kwargs):
            return Safe(kwargs["asset"], kwargs["id"]).modify(data=kwargs["data"])

        return self.modify(
            technology=["cyberark"],
            request=request,
            actionCall=actionCall,
            objectUid=id,
            doLock=False
        )
