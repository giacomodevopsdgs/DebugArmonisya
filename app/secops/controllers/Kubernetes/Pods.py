from rest_framework.request import Request
from rest_framework.response import Response

from secops.models.Kubernetes.Pod import Pod

from secops.controllers.CustomController import CustomController


class PodsController(CustomController):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="kubernetes_resource", *args, **kwargs)



    def get(self, request: Request) -> Response:
        def actionCall(**kwargs):
            return Pod.rawDataList(**kwargs)

        return self.ls(
            technology=["kubernetes"],
            request=request,
            actionCall=actionCall
        )
