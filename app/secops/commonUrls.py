from django.urls import path

from secops.controllers import Root
from secops.controllers.Asset import Asset, Assets
from secops.controllers.Permission import Authorizations, IdentityGroups, IdentityGroup, Roles, Permission, Permissions


urlpatterns = [
    path("", Root.RootController.as_view()),

    # Asset.
    path("assets/", Assets.AssetsController.as_view(), name="secops-assets"),
    path("asset/<int:assetId>/", Asset.AssetController.as_view(), name="secops-asset"),

    # Permissions.
    path("identity-groups/", IdentityGroups.PermissionIdentityGroupsController.as_view(), name="permission-identity-groups"),
    path("identity-group/<str:identityGroupIdentifier>/", IdentityGroup.PermissionIdentityGroupController.as_view(), name="permission-identity-group"),
    path("roles/", Roles.PermissionRolesController.as_view(), name="permission-roles"),
    path("permissions/", Permissions.PermissionsController.as_view(), name="permissions"),
    path("permission/<int:permissionId>/", Permission.PermissionController.as_view(), name="permission"),
    path("authorizations/", Authorizations.AuthorizationsController.as_view(), name="authorizations"),
]
