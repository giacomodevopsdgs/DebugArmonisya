from rest_framework.request import Request
from rest_framework.response import Response

from secops.models.Conjur.Variable import Variable

from secops.controllers.CustomController import CustomController


class VariableController(CustomController):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="conjur_resource", *args, **kwargs)



    def get(self, request: Request, variableId: str) -> Response:
        def actionCall(**kwargs):
            return Variable(**kwargs).repr()

        return self.info(
            technology=["conjur"],
            request=request,
            actionCall=actionCall,
            objectUid=variableId
        )



    def post(self, request: Request, variableId: str) -> Response:
        def actionCall(**kwargs):
            return Variable(kwargs["asset"], kwargs["id"]).addSecret(data=kwargs["data"])

        return self.modify(
            technology=["conjur"],
            request=request,
            actionCall=actionCall,
            objectUid=variableId
        )
