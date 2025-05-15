import json
from base64 import b64encode


class Session:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def getConjurLogon(asset: dict, accessType: str) -> str:
        from secops.helpers.ApiSupplicant import ApiSupplicant

        try:
            apiKey = ApiSupplicant(
                asset=asset,
                endpoint=f"authn/{asset.get('account', '')}/login/",
                accessType=accessType,
                headers={
                    "Authorization": "Basic " + b64encode((asset.get("username", "") + ":" + asset.get("password", "")).encode()).decode("ascii")
                },
                silent=True,
                handlingSession=True
            ).get()["payload"]

            jwtInformation = ApiSupplicant(
                asset=asset,
                endpoint=f"authn/{asset.get('account', '')}/admin/authenticate/",
                accessType=accessType,
                data=apiKey,
                jsonPayload=False,
                silent=True,
                handlingSession=True
            ).post()["payload"]

            return b64encode(json.dumps(jwtInformation).encode()).decode("ascii")
        except Exception as e:
            raise e
