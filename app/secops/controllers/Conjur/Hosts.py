from rest_framework.request import Request
from rest_framework.response import Response

from secops.models.Conjur.Host import Host

from secops.controllers.CustomController import CustomController


class HostsController(CustomController):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="conjur_resource", *args, **kwargs)



    def get(self, request: Request) -> Response:
        def actionCall(**kwargs):
            return Host.rawDataList(**kwargs)

        return self.ls(
            technology=["conjur"],
            request=request,
            actionCall=actionCall
        )
