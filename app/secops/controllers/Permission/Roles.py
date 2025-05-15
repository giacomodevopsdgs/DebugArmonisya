from rest_framework.request import Request
from rest_framework.response import Response

from secops.models.Permission.Role import Role

from secops.serializers.Permission.Roles import RolesSerializer as Serializer

from secops.controllers.CustomController import CustomController


class PermissionRolesController(CustomController):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="role", *args, **kwargs)



    def get(self, request: Request) -> Response:
        def actionCall(**kwargs):
            loadPrivilege = False
            if "related" in request.GET:
                rList = request.GET.getlist('related')
                if "privileges" in rList:
                    loadPrivilege = True

            return [
                r.repr() for r in Role.list(loadPrivilege=loadPrivilege)
            ]

        return self.ls(
            request=request,
            actionCall=actionCall,
            Serializer=Serializer,
            doLock=False
        )
