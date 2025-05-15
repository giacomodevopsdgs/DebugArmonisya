from rest_framework.request import Request
from rest_framework.response import Response

from secops.controllers.CustomController import CustomController

from secops.models.Asset.Asset import Asset

from secops.serializers.Asset.Asset import AssetSerializer
from secops.serializers.Asset.Assets import AssetsSerializer


class AssetsController(CustomController):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="asset", *args, **kwargs)



    def get(self, request: Request) -> Response:
        def actionCall(**kwargs):
            return Asset.rawDataList(showPassword=False)

        return self.ls(
            request=request,
            actionCall=actionCall,
            Serializer=AssetsSerializer,
            doLock=False
        )



    def post(self, request: Request) -> Response:
        def actionCall(**kwargs):
            return Asset.add(data=kwargs["data"])

        return self.add(
            request=request,
            actionCall=actionCall,
            Serializer=AssetSerializer,
            doLock=False
        )
