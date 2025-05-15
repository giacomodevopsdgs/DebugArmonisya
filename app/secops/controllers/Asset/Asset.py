from rest_framework.request import Request
from rest_framework.response import Response

from secops.controllers.CustomController import CustomController

from secops.models.Asset.Asset import Asset

from secops.serializers.Asset.Asset import AssetSerializer


class AssetController(CustomController):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="asset", *args, **kwargs)



    def get(self, request: Request, assetId: int) -> Response:
        def actionCall(**kwargs):
            return Asset(kwargs["id"], showPassword=False).repr()

        return self.info(
            request=request,
            actionCall=actionCall,
            objectUid=str(assetId),
            Serializer=AssetSerializer,
            doLock=False
        )



    def delete(self, request: Request, assetId: int) -> Response:
        def actionCall(**kwargs):
            return Asset(kwargs["id"]).delete()

        return self.remove(
            request=request,
            actionCall=actionCall,
            objectUid=str(assetId),
            doLock=False
        )



    def patch(self, request: Request, assetId: int) -> Response:
        def actionCall(**kwargs):
            return Asset(kwargs["id"]).modify(data=kwargs["data"])

        return self.modify(
            request=request,
            actionCall=actionCall,
            objectUid=str(assetId),
            Serializer=AssetSerializer,
            doLock=False
        )
