from rest_framework.request import Request
from rest_framework.response import Response

from secops.models.Permission.IdentityGroup import IdentityGroup

from secops.serializers.Permission.IdentityGroup import IdentityGroupSerializer as GroupSerializer

from secops.controllers.CustomController import CustomController


class PermissionIdentityGroupController(CustomController):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="permission_identityGroup", *args, **kwargs)



    def delete(self, request: Request, identityGroupIdentifier: str) -> Response:
        def actionCall(**kwargs):
            return IdentityGroup(identityGroupIdentifier=kwargs["id"]).delete()

        return self.remove(
            request=request,
            actionCall=actionCall,
            objectUid=identityGroupIdentifier,
            doLock=False
        )



    def patch(self, request: Request, identityGroupIdentifier: str) -> Response:
        def actionCall(**kwargs):
            return IdentityGroup(identityGroupIdentifier=kwargs["id"]).modify(data=kwargs["data"])

        return self.modify(
            request=request,
            actionCall=actionCall,
            objectUid=identityGroupIdentifier,
            Serializer=GroupSerializer,
            doLock=False
        )
