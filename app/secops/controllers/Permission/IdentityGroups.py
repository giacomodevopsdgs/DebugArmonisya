from rest_framework.request import Request
from rest_framework.response import Response

from secops.models.Permission.IdentityGroup import IdentityGroup

from secops.serializers.Permission.IdentityGroups import IdentityGroupsSerializer as GroupsSerializer
from secops.serializers.Permission.IdentityGroup import IdentityGroupSerializer as GroupSerializer

from secops.controllers.CustomController import CustomController


class PermissionIdentityGroupsController(CustomController):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="permission_identityGroup", *args, **kwargs)



    def get(self, request: Request) -> Response:
        def actionCall(**kwargs):
            return [
                ig.repr() for ig in IdentityGroup.list()
            ]

        return self.ls(
            request=request,
            actionCall=actionCall,
            Serializer=GroupsSerializer,
            doLock=False
        )



    def post(self, request: Request) -> Response:
        def actionCall(**kwargs):
            IdentityGroup.add(data=kwargs["data"])

        return self.add(
            request=request,
            actionCall=actionCall,
            Serializer=GroupSerializer,
            doLock=False
        )
