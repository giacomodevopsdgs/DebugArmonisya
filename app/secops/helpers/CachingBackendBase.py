from typing import Optional, Union
from hashlib import md5

from django.conf import settings
from django.core.cache import cache

from secops.helpers.ApiSupplicant import ApiSupplicant
from secops.helpers.Log import Log


class CachingBackendBase:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def get(noCache: bool = False, **kwargs) -> Union[list, dict]:
        try:
            if noCache or not settings.CACHE_ENABLE:
                # Force fetching data and update cache.
                o = ApiSupplicant(**kwargs).get()["payload"]
            else:
                # Read data from cache, if available.
                # Otherwise, remotely fetch (and do caching).
                cachedContent = CachingBackendBase.__cacheHandler(operation="l", method="GET", **kwargs)
                if cachedContent:
                    o = cachedContent
                else:
                    o = ApiSupplicant(**kwargs).get()["payload"]
                    CachingBackendBase.__cacheHandler(operation="s", o=o, method="GET", **kwargs)

            return o
        except Exception as e:
            raise e



    @staticmethod
    def post(forceCache: bool = False, **kwargs) -> dict:
        try:
            if forceCache:
                cachedContent = CachingBackendBase.__cacheHandler(operation="l", method="POST", **kwargs)
                if cachedContent:
                    o = cachedContent
                else:
                    o = ApiSupplicant(**kwargs).post()
                    CachingBackendBase.__cacheHandler(operation="s", o=o, method="POST", **kwargs)
            else:
                o = ApiSupplicant(**kwargs).post()

            return o
        except Exception as e:
            raise e



    @staticmethod
    def patch(**kwargs) -> None:
        try:
            ApiSupplicant(**kwargs).patch()
        except Exception as e:
            raise e



    @staticmethod
    def put(**kwargs) -> Union[dict, str]:
        try:
            return ApiSupplicant(**kwargs).put()["payload"]
        except Exception as e:
            raise e



    @staticmethod
    def delete(**kwargs) -> None:
        try:
            ApiSupplicant(**kwargs).delete()
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private static methods
    ####################################################################################################################

    @staticmethod
    def __cacheHandler(operation: str, **kwargs) -> Optional[object]:
        try:
            # Cache element id must contain the apikey, for different assets usually connect to the same endpoint: apiKey is the differentiating element.
            # Objection: in secops an apikey can be relative to only one asset, so the assetId is enough to differentiate the cache elements.
            e = md5(str(kwargs["method"] + kwargs["endpoint"] + str(kwargs.get("data", None))).encode("utf-8")).hexdigest()

            if operation == "l":
                cachedContent = cache.get(e)
                if cachedContent:
                    Log.actionLog("[CachingBackendBase] Content loaded from cache")
                return cachedContent

            if operation == "s":
                cache.set(e, kwargs.get("o", None), timeout=settings.REMOTE_CACHE_VALIDITY_FOR_DATA)
                Log.actionLog("[CachingBackendBase] Content cached")
        except Exception as e:
            raise e
