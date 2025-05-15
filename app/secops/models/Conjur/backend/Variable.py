from secops.models.Conjur.backend.Resource import Resource

from secops.helpers.CachingBackendBase import CachingBackendBase
from secops.helpers.Exception import CustomException


class Variable(Resource):

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def addSecret(asset: dict, id: str, data: dict, **kwargs) -> None:
        accessType = "conjur"

        try:
            endpoint = f"secrets/{asset.get('account', '')}/variable/{id.split(':')[2]}"
            CachingBackendBase.post(
                asset=asset,
                endpoint=endpoint,
                accessType=accessType,
                data=data.get("secrets", ""),
                jsonPayload=False,
                **kwargs
            )
        except IndexError:
            raise CustomException(status=409)
        except Exception as e:
            raise e
