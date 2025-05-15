import functools

from django.urls import resolve

from secops.models.History.ActionHistory import ActionHistory as History

from secops.controllers.CustomControllerBase import CustomControllerBase


def historyLog(method):
    @functools.wraps(method)
    def w(methodSelf, *methodArgs, **methodKwargs):
        # Run the wrapped method.
        o = method(methodSelf, *methodArgs, **methodKwargs)

        # Log.
        if "assetId" in methodKwargs:
            try:
                History.add({
                    "asset_id": int(methodKwargs["assetId"]),
                    "action": resolve(methodKwargs["request"].path).url_name + '_' + methodKwargs["request"].method.lower(),
                    "response_status": int(o.status_code),
                    "username": CustomControllerBase.loggedUser(methodKwargs["request"]).get("username", "")
                })
            except Exception:
                pass

        return o
    return w
