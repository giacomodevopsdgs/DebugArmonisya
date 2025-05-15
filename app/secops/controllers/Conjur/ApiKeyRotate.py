from rest_framework.request import Request
from rest_framework.response import Response

from secops.models.Conjur.Apikey import Apikey

from secops.controllers.CustomController import CustomController


class ApiKeyRotateController(CustomController):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="conjur_resource", *args, **kwargs)



    def put(self, request: Request, apikeyId: str) -> Response:
        def actionCall(**kwargs):
            return Apikey.rotate(**kwargs)

        return self.modify(
            technology=["conjur"],
            request=request,
            objectUid=apikeyId,
            actionCall=actionCall
        )
