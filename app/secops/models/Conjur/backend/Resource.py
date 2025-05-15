from secops.helpers.CachingBackendBase import CachingBackendBase
from secops.helpers.Exception import CustomException


class Resource:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def get(asset: dict, resource: str, id: str, **kwargs) -> dict:
        try:
            try:
                el = Resource.list(resource=resource, asset=asset, filter=id, **kwargs)[0]
            except IndexError:
                raise CustomException(status=404)
        except Exception as e:
            raise e

        return el



    @staticmethod
    def list(asset: dict, resource: str, filter: str = "", noCache: bool = False, **kwargs) -> list:
        o = []
        offset = 0

        endpoint = f"resources/{asset.get('account', '')}/?kind={resource}"
        accessType = "conjur"

        try:
            while True:
                if filter:
                    partialEndpoint = endpoint + f"&limit=1000&offset={offset}&search={filter}" # paginate.
                else:
                    partialEndpoint = endpoint + f"&limit=1000&offset={offset}" # paginate.

                partial = CachingBackendBase.get(
                    asset=asset,
                    endpoint=partialEndpoint,
                    accessType=accessType,
                    noCache=noCache,
                    **kwargs
                )

                if partial:
                    o.extend(partial)
                    offset += 1000
                else:
                    break

            return o
        except Exception as e:
            raise e
