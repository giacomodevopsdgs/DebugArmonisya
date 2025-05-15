from secops.helpers.CachingBackendBase import CachingBackendBase


class Apikey:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def rotate(asset: dict, id: str, data: dict = None, **kwargs) -> str:
        endpoint = f"authn/{asset.get('account', '')}/api_key/?role={id}"
        accessType = "conjur"

        try:
            return CachingBackendBase.put(
                asset=asset,
                endpoint=endpoint,
                accessType=accessType,
                data=None,
                **kwargs
            )
        except Exception as e:
            raise e
