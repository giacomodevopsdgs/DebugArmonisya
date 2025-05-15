from rest_framework.request import Request
from rest_framework.response import Response

from secops.models.CyberArk.Safe import Safe

from secops.controllers.CustomController import CustomController


class SafesController(CustomController):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="cyberark_safe", *args, **kwargs)



    def get(self, request: Request) -> Response:
        def actionCall(**kwargs):
            return Safe.rawDataList(**kwargs)

        return self.ls(
            technology=["cyberark"],
            request=request,
            actionCall=actionCall
        )



    def post(self, request: Request) -> Response:
        def actionCall(**kwargs):
            return Safe.add(**kwargs)

        return self.add(
            technology=["cyberark"],
            request=request,
            actionCall=actionCall
        )
