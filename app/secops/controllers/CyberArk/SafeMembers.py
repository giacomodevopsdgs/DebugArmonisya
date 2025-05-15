from rest_framework.request import Request
from rest_framework.response import Response

from secops.models.CyberArk.Safe import Safe

from secops.controllers.CustomController import CustomController


class SafeMembersController(CustomController):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="cyberark_safe", *args, **kwargs)



    def get(self, request: Request, id: str) -> Response:
        def actionCall(**kwargs):
            return Safe(id=kwargs["parentId"], **kwargs).membersRawDataList()

        return self.ls(
            technology=["cyberark"],
            request=request,
            parentId=id,
            actionCall=actionCall
        )



    def post(self, request: Request, id: str) -> Response:
        def actionCall(**kwargs):
            return Safe(id=kwargs["parentId"], **kwargs).addMember(data=kwargs["data"])

        return self.add(
            technology=["cyberark"],
            request=request,
            parentId=id,
            actionCall=actionCall
        )
