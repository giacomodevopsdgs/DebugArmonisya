from secops.models.Conjur.backend.Resource import Resource

from secops.helpers.CachingBackendBase import CachingBackendBase


class Policy(Resource):

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def add(asset: dict, parentId: str, data: dict, **kwargs) -> None:
        branch = parentId
        endpoint = f"policies/{asset.get('account', '')}/policy/{branch}"
        accessType = "conjur"

        try:
            CachingBackendBase.post(
                asset=asset,
                endpoint=endpoint,
                accessType=accessType,
                data=data,
                jsonPayload=False,
                **kwargs
            )
        except Exception as e:
            raise e
