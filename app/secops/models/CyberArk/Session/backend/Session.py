from django.conf import settings

from secops.helpers.Log import Log


class Session:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def getCyberArkCredentialsThroughCCP(asset: dict, accessType: str) -> str:
        from secops.helpers.ApiSupplicant import ApiSupplicant

        # https://docs.cyberark.com/credential-providers/latest/en/content/ccp/calling-the-web-service-using-rest.htm?tocpath=Developer%7CCentral%20Credential%20Provider%20(CCP)%7CCall%20the%20Central%20Credential%20Provider%20Web%20Service%20from%20Your%20Application%20Code%7C_____2

        try:
            return ApiSupplicant(
                asset=asset,
                endpoint="accounts?AppID=" + asset.get("appId", "") + "&Username=" + asset.get("ccpUsername", ""),
                certificates=(settings.CERTIFICATES_ROOT + "ccp.crt", settings.CERTIFICATES_ROOT + "ccp.key"),
                accessType=accessType,
                silent=True,
                handlingSession=True
            ).get()["payload"].get("Content", "")
        except Exception as e:
            raise e



    @staticmethod
    def getCyberArkLogon(asset: dict, accessType: str) -> str:
        from secops.helpers.ApiSupplicant import ApiSupplicant

        try:
            return ApiSupplicant(
                asset=asset,
                endpoint="auth/Cyberark/Logon/",
                accessType=accessType,
                data={
                    "username": asset.get("username", ""),
                    "password": asset.get("password", ""),
                    "concurrentSession": True
                },
                silent=True,
                handlingSession=True
            ).post()["payload"]
        except Exception as e:
            raise e



    @staticmethod
    def CyberArkLogoff(asset: dict, accessType: str, accessToken: str) -> None:
        from secops.helpers.ApiSupplicant import ApiSupplicant

        try:
            ApiSupplicant(
                asset=asset,
                accessType=accessType,
                headers={
                    "Authorization": accessToken
                },
                endpoint="auth/Logoff/",
                handlingSession=True
            ).post()
        except Exception as e:
            raise e
