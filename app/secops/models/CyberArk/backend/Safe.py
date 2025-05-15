from secops.helpers.CachingBackendBase import CachingBackendBase


class Safe:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def get(asset: dict, safeUrlId: str, **kwargs) -> dict:
        endpoint = "Safes/" + str(safeUrlId) + "/"
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
    def list(asset: dict, **kwargs) -> list:
        o = []
        offset = 0

        endpoint = "Safes/"
        accessType = "cyberark"

        try:
            while True:
                partialEndpoint = endpoint + f"?limit=100&offset={offset}&useCache=False" # paginate.
                partial = CachingBackendBase.get(
                    asset=asset,
                    endpoint=partialEndpoint,
                    accessType=accessType,
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
    def add(asset: dict, data: dict, **kwargs) -> list:
        endpoint = "Safes/"
        accessType = "cyberark"

        try:
            return CachingBackendBase.post(
                asset=asset,
                endpoint=endpoint,
                accessType=accessType,
                data=data,
                **kwargs
            )
        except Exception as e:
            raise e



    @staticmethod
    def modify(asset: dict, safeUrlId: str, data: dict, **kwargs) -> list:
        endpoint = "Safes/" + str(safeUrlId) + "/"
        accessType = "cyberark"

        try:
            return CachingBackendBase.put(
                asset=asset,
                endpoint=endpoint,
                accessType=accessType,
                data=data,
                **kwargs
            )
        except Exception as e:
            raise e



    @staticmethod
    def delete(asset: dict, safeUrlId: str, **kwargs) -> None:
        endpoint = "Safes/" + str(safeUrlId) + "/"
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



    @staticmethod
    def members(asset: dict, safeUrlId: str, **kwargs) -> list:
        o = []
        offset = 0

        endpoint = "Safes/" + str(safeUrlId) + "/Members/"
        accessType = "cyberark"

        try:
            while True:
                partialEndpoint = endpoint + f"?limit=100&offset={offset}&useCache=False" # paginate.
                partial = CachingBackendBase.get(
                    asset=asset,
                    endpoint=partialEndpoint,
                    accessType=accessType,
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
    def addMember(asset: dict,  safeUrlId: str, data: dict, **kwargs) -> dict:
        endpoint = "Safes/" + str(safeUrlId) + "/Members/"
        accessType = "cyberark"

        try:
            return CachingBackendBase.post(
                asset=asset,
                endpoint=endpoint,
                accessType=accessType,
                data=data,
                **kwargs
            )
        except Exception as e:
            raise e



    @staticmethod
    def addAccount(asset: dict, safeName: str, data: dict, **kwargs) -> dict:
        endpoint = "Accounts/"
        accessType = "cyberark"

        data["safeName"] = safeName

        try:
            return CachingBackendBase.post(
                asset=asset,
                endpoint=endpoint,
                accessType=accessType,
                data=data,
                **kwargs
            )["payload"]
        except Exception as e:
            raise e
