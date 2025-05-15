from django.conf import settings
from django.core.cache import cache

from secops.models.Conjur.Session.backend.Session import Session as Backend

from secops.helpers.Log import Log


class Session:

    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    @staticmethod
    def getConjurSessionToken(sessionUid: str, asset: dict) -> str:
        key = "conjur-session-token-" + str(sessionUid) + "-" + str(asset["technology"])

        try:
            cachedToken = cache.get(key)
            if cachedToken:
                token = cachedToken
            else:
                token = "Token token=\"" + Backend.getConjurLogon(asset, "conjur") + "\""
                cache.set(key, token, timeout=settings.REMOTE_CACHE_VALIDITY_FOR_AUTH)
        except Exception as e:
            raise e

        return token



    @staticmethod
    def delete(sessionUid: str, asset: dict) -> None:
        try:
            key = "conjur-session-token-" + str(sessionUid) + "-" + str(asset["technology"])
            cachedToken = cache.get(key)
            if cachedToken:
                cache.delete(key)
                Log.log("[SESSION CyberArk API] Deleted session: " + str(sessionUid))
        except Exception as e:
            raise e
