from django.urls import re_path, path

from secops.controllers.Conjur import Users, Hosts, Layers, Groups, Variables, Variable, Webservices, Policies, ApiKeyRotate


urlpatterns = [
    path("users/", Users.UsersController.as_view(), name="conjur-users"),

    path("hosts/", Hosts.HostsController.as_view(), name="conjur-hosts"),

    path("layers/", Layers.LayersController.as_view(), name="conjur-layers"),

    path("groups/", Groups.GroupsController.as_view(), name="conjur-groups"),

    path("policies/", Policies.PoliciesController.as_view(), name="conjur-policies"),
    re_path("^policies/branch/(?P<branchId>.*)/$", Policies.PoliciesController.as_view(), name="conjur-policies"),

    path("variables/", Variables.VariablesController.as_view(), name="conjur-variables"),
    re_path("^variable/(?P<variableId>.*)/$", Variable.VariableController.as_view(), name="conjur-variable"),

    path("webservices/", Webservices.WebservicesController.as_view(), name="conjur-webservices"),

    re_path("^rotate-apikey/(?P<apikeyId>.*)/$", ApiKeyRotate.ApiKeyRotateController.as_view(), name="conjur-apikey-rotate"),
]
