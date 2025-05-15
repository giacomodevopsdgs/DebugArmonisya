from rest_framework.request import Request
from rest_framework.response import Response

from secops.models.Permission.Permission import Permission

from secops.serializers.Permission.Permission import PermissionSerializer as Serializer

from secops.controllers.CustomController import CustomController


class PermissionController(CustomController):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="permission_identityGroup", *args, **kwargs)



    def delete(self, request: Request, permissionId: int) -> Response:
        def actionCall(**kwargs):
            return Permission(int(kwargs["id"])).delete()

        return self.remove(
            request=request,
            actionCall=actionCall,
            objectUid=str(permissionId),
            doLock=False
        )



    def patch(self, request: Request, permissionId: int) -> Response:
        def actionCall(**kwargs):
            return Permission.modifyFacade(
                permissionId=int(kwargs["id"]),
                identityGroupId=kwargs["data"].get("identity_group_identifier", ""),
                role=kwargs["data"].get("role", "")
            )

        return self.modify(
            request=request,
            actionCall=actionCall,
            objectUid=str(permissionId),
            Serializer=Serializer,
            doLock=False
        )
