from secops.helpers.RepositoryBase import RepositoryBase


class Asset:

    # Table: asset

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def get(assetId: int, showPassword: bool) -> dict:
        fields = "id, technology, fqdn, protocol, port, path, tlsverify, baseurl, account, IFNULL (datacenter, '') AS datacenter, environment, IFNULL (position, '') AS position, IFNULL (certificate_authority_data, '') AS certificate_authority_data"
        if showPassword:
            fields += ", IFNULL (appid, '') AS appid, IFNULL (username, '') AS username, IFNULL (password, '') AS password, IFNULL (repokey, '') AS repokey, IFNULL (userkey, '') AS userkey, IFNULL (client_certificate_data, '') AS client_certificate_data, IFNULL (client_key_data, '') AS client_key_data"

        try:
            info = RepositoryBase.get(
                table="asset",
                select=fields,
                where=[("id", assetId, "int")]
            )
            info["tlsverify"] = bool(info["tlsverify"])

            return info
        except Exception as e:
            raise e



    @staticmethod
    def list(showPassword: bool) -> list:
        fields = "id, technology, fqdn, protocol, port, path, tlsverify, baseurl, account, IFNULL (datacenter, '') AS datacenter, environment, IFNULL (position, '') AS position, IFNULL (certificate_authority_data, '') AS certificate_authority_data"
        if showPassword:
            fields += ", IFNULL (appid, '') AS appid, IFNULL (username, '') AS username, IFNULL (password, '') AS password, IFNULL (repokey, '') AS repokey, IFNULL (userkey, '') AS userkey, IFNULL (client_certificate_data, '') AS client_certificate_data, IFNULL (client_key_data, '') AS client_key_data"

        try:
            l = RepositoryBase.list(
                table="asset",
                select=fields
            )
            for el in l:
                el["tlsverify"] = bool(el["tlsverify"])

            return l
        except Exception as e:
            raise e



    @staticmethod
    def add(data: dict) -> None:
        try:
            if "tlsverify" in data:
                data["tlsverify"] = int(data["tlsverify"])

            assetInfo = RepositoryBase.add(table="asset", data=data, allowHtmlFields=["username", "password"])
            RepositoryBase.modify(table="asset", id=assetInfo["id"], data={
                "baseurl": Asset.__getBaseurl(assetInfo["id"])
            })
        except Exception as e:
            raise e



    @staticmethod
    def modify(assetId: int, data: dict) -> None:
        try:
            if "tlsverify" in data:
                data["tlsverify"] = int(data["tlsverify"])

            RepositoryBase.modify(table="asset", id=assetId, data=data, allowHtmlFields=["username", "password"])
            RepositoryBase.modify(table="asset", id=assetId, data={
                "baseurl": Asset.__getBaseurl(assetId)
            })
        except Exception as e:
            raise e



    @staticmethod
    def delete(assetId: int) -> None:
        try:
            return RepositoryBase.delete(table="asset", id=assetId)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private static methods
    ####################################################################################################################

    @staticmethod
    def __getBaseurl(assetId: int) -> str:
        ai = Asset.get(assetId, showPassword=True)

        if ai["technology"] == "cyberark" or ai["technology"] == "conjur" or ai["technology"] == "kubernetes":
            baseurl = f"{ai['protocol']}://{ai['fqdn']}:{ai['port']}{ai['path']}"

        elif ai["technology"] == "git":
            if "environment" in ai:
                baseurl = f"{ai['username']}@{ai['fqdn']}:{ai['environment']}{ai['path']}"
            else:
                baseurl = f"{ai['username']}@{ai['fqdn']}:{ai['port']}{ai['path']}"

        else:
            raise NotImplemented

        return baseurl
