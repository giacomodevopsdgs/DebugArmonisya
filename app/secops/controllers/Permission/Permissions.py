from rest_framework.request import Request
from rest_framework.response import Response

from secops.models.Permission.Permission import Permission

from secops.serializers.Permission.Permissions import PermissionsSerializer as PermissionsSerializer
from secops.serializers.Permission.Permission import PermissionSerializer as PermissionSerializer

from secops.controllers.CustomController import CustomController


class PermissionsController(CustomController):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="permission_identityGroup", *args, **kwargs)



    def get(self, request: Request) -> Response:
        def actionCall(**kwargs):
            return Permission.permissionsDataList()

        return self.ls(
            request=request,
            actionCall=actionCall,
            Serializer=PermissionsSerializer,
            doLock=False
        )



    def post(self, request: Request) -> Response:
        def actionCall(**kwargs):
            Permission.addFacade(
                identityGroupId=kwargs["data"].get("identity_group_identifier", ""),
                role=kwargs["data"].get("role", "")
            )

        return self.add(
            request=request,
            actionCall=actionCall,
            Serializer=PermissionSerializer,
            doLock=False
        )
