from rest_framework.request import Request
from rest_framework.response import Response

from secops.models.Conjur.Policy import Policy

from secops.controllers.CustomController import CustomController


class PoliciesController(CustomController):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="conjur_resource", *args, **kwargs)



    def get(self, request: Request) -> Response:
        def actionCall(**kwargs):
            return Policy.rawDataList(resource="policy", **kwargs)

        return self.ls(
            technology=["conjur"],
            request=request,
            actionCall=actionCall
        )



    def post(self, request: Request, branchId: str) -> Response:
        def actionCall(**kwargs):
            return Policy.add(**kwargs)

        return self.add(
            technology=["conjur"],
            request=request,
            parentId=branchId,
            actionCall=actionCall
        )
