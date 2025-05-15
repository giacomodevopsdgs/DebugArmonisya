from rest_framework.request import Request
from rest_framework.response import Response

from secops.usercases.BPER import BPER

from secops.controllers.CustomController import CustomController

from secops.helpers.Exception import CustomException


class UseCaseBPERController(CustomController):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="usecase_bper", *args, **kwargs)



    def post(self, request: Request, action: str) -> Response:
        def actionCall(**kwargs):
            if action in ("cyberark-insert", "cyberark-modify"):
                params = dict()
                for k in ("vault", "safe", "accounts", "app", "ticket"):
                    params[k] = kwargs["data"].get(k, {})

                del kwargs["data"]
                kwargs.update(params) # **kwargs contains usual CustomController data, together with params.

                return BPER(**kwargs)(action)
            else:
                raise CustomException(status=400)

        return self.run(
            technology=["cyberark", "git"],
            request=request,
            actionCall=actionCall
        )
