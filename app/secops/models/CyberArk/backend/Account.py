from secops.helpers.CachingBackendBase import CachingBackendBase
from secops.helpers.decorators.UserFilters import userFilters


class Account:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def get(asset: dict, id: str, **kwargs) -> dict:
        endpoint = "Accounts/" + str(id) + "/"
        accessType = "cyberark"

        try:
            return CachingBackendBase.get(
                asset=asset,
                endpoint=endpoint,
                accessType=accessType,
                **kwargs
            )
        except Exception as e:
            raise e



    @staticmethod
    @userFilters
    def list(asset: dict, safeName: str = "", noCache: bool = False, **kwargs) -> list:
        o = []
        offset = 0

        endpoint = "Accounts/"
        accessType = "cyberark"

        filter = ""
        if safeName:
            filter = f"safeName eq {safeName}"

        try:
            while True:
                partialEndpoint = endpoint + f"?limit=100&offset={offset}&useCache=False&filter={filter}" # paginate.
                partial = CachingBackendBase.get(
                    asset=asset,
                    endpoint=partialEndpoint,
                    accessType=accessType,
                    noCache=noCache,
                    **kwargs
                )

                content = partial.get("value", [])
                if content:
                    o.extend(content)

                if "nextLink" in partial:
                    offset += 100
                else:
                    break

            return o
        except Exception as e:
            raise e



    @staticmethod
    def modify(asset: dict, id: str, data: dict, **kwargs) -> list:
        accessType = "cyberark"

        # Turn data dict into the stupid structure below.
        # https://docs.cyberark.com/pam-self-hosted/latest/en/content/sdk/updateaccount%20v10.htm?tocpath=Developer%7CREST%20APIs%7CAccounts%7C_____7
        #    {
        #       "op":"replace",
        #       "path":"/address",
        #       "value":"NewAddress"
        #    },
        #
        # In case of secret change, a different URL must be called: /Password/Update/ (wtf).

        try:
            if "secret" in data:
                endpoint = "Accounts/" + str(id) + "/Password/Update/"
                return CachingBackendBase.post(
                    asset=asset,
                    endpoint=endpoint,
                    accessType=accessType,
                    data={
                        "NewCredentials": data["secret"]
                    },
                    **kwargs
                )
            else:
                sillyData = list()

                endpoint = "Accounts/" + str(id) + "/"
                for k, v in data.items():
                    sillyData.append({
                        "op": "replace",
                        "path": f"/{k}",
                        "value": v
                    })

                return CachingBackendBase.patch(
                    asset=asset,
                    endpoint=endpoint,
                    accessType=accessType,
                    data=sillyData,
                    **kwargs
                )
        except Exception as e:
            raise e



    @staticmethod
    def delete(asset: dict, id: str, **kwargs) -> None:
        endpoint = "Accounts/" + str(id) + "/"
        accessType = "cyberark"

        try:
            CachingBackendBase.delete(
                asset=asset,
                endpoint=endpoint,
                accessType=accessType,
                **kwargs
            )
        except Exception as e:
            raise e
