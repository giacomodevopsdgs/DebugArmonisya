from rest_framework.request import Request
from rest_framework.response import Response

from secops.models.Permission.Permission import Permission
from secops.controllers.CustomController import CustomController


class AuthorizationsController(CustomController):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="authorization", *args, **kwargs)



    def get(self, request: Request) -> Response:
        # Enlist caller's permissions (depending on groups user belongs to).

        def actionCall(**kwargs):
            user = CustomController.loggedUser(request)
            if not user["authDisabled"]:
                return Permission.authorizationsDataList(user["groups"])
            else:
                return ["any"]

        return self.ls(
            request=request,
            actionCall=actionCall,
            openCall=True, # anyone logged can view their permissions.
            doLock=False,
        )
