from rest_framework.request import Request
from rest_framework.response import Response

from secops.models.CyberArk.Account import Account

from secops.controllers.CustomController import CustomController


class AccountsController(CustomController):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="cyberark_account", *args, **kwargs)



    def get(self, request: Request) -> Response:
        def actionCall(**kwargs):
            return Account.rawDataList(**kwargs)

        return self.ls(
            technology=["cyberark"],
            request=request,
            actionCall=actionCall
        )
