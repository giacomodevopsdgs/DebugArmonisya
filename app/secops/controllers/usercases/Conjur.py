from rest_framework.request import Request
from rest_framework.response import Response

from secops.usercases.Conjur import Conjur

from secops.controllers.CustomController import CustomController

from secops.helpers.Exception import CustomException


class UseCaseConjurController(CustomController):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="usecase_conjur", *args, **kwargs)



    def get(self, request: Request, action: str) -> Response:
        def actionCall(**kwargs):
            if action in ("verify-git-policy", ):
                return Conjur(**kwargs)(action)
            else:
                raise CustomException(status=400)

        return self.run(
            technology=["conjur", "kubernetes", "git"],
            request=request,
            actionCall=actionCall
        )



    def post(self, request: Request, action: str) -> Response:
        def actionCall(**kwargs):
            if action in ("align-git-policy", ):
                params = dict()
                for k in ("vault", "conjur"):
                    params[k] = kwargs["data"].get(k, {})

                del kwargs["data"]
                kwargs.update(params) # **kwargs contains usual CustomController data, together with params.

                return Conjur(**kwargs)(action)
            else:
                raise CustomException(status=400)

        return self.run(
            technology=["conjur", "kubernetes", "git"],
            request=request,
            actionCall=actionCall
        )
