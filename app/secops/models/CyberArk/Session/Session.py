from django.conf import settings
from django.core.cache import cache

from secops.models.CyberArk.Session.backend.Session import Session as Backend

from secops.helpers.Log import Log


class Session:

    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    @staticmethod
    def getCyberArkCredentialsThroughCCP(asset: dict):
        try:
            password = Backend.getCyberArkCredentialsThroughCCP(asset, "cyberark-ccp")
        except Exception as e:
            raise e

        return password



    @staticmethod
    def getCyberArkSessionToken(sessionUid: str, asset: dict) -> str:
        key = "cyberark-session-token-" + str(sessionUid) + "-" + str(asset["technology"])

        try:
            cachedToken = cache.get(key)
            if cachedToken:
                token = cachedToken
            else:
                asset["password"] = Session.getCyberArkCredentialsThroughCCP(asset)
                token = Backend.getCyberArkLogon(asset, "cyberark")
                cache.set(key, token, timeout=settings.REMOTE_CACHE_VALIDITY_FOR_AUTH)
        except Exception as e:
            raise e

        return token



    @staticmethod
    def delete(sessionUid: str, asset: dict) -> None:
        try:
            # Deleting session for CyberArk API, if existent.
            key = "cyberark-session-token-" + str(sessionUid) + "-" + str(asset["technology"])
            cachedToken = cache.get(key)
            if cachedToken:
                cache.delete(key)

                try:
                    Backend.CyberArkLogoff(asset, "cyberark", cachedToken)
                    Log.log("[SESSION CyberArk API] Deleted session: " + str(sessionUid))
                except Exception:
                    pass
        except Exception as e:
            raise e
