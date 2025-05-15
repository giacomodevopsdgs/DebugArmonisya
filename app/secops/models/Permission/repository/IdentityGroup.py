from secops.helpers.RepositoryBase import RepositoryBase


class IdentityGroup:

    # Table: identity_group

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def get(id: int, identityGroupIdentifier: str) -> dict:
        where = []
        if id:
            where = [("id", id, "int")]
        if identityGroupIdentifier:
            where = [("identity_group_identifier", identityGroupIdentifier, "string")]

        try:
            return RepositoryBase.get(
                table="identity_group",
                select="id, name, identity_group_identifier",
                where=where
            )
        except Exception as e:
            raise e



    @staticmethod
    def modify(id: int, data: dict) -> None:
        try:
            RepositoryBase.modify(table="identity_group", id=id, data=data)
        except Exception as e:
            raise e



    @staticmethod
    def delete(id: int) -> None:
        try:
            return RepositoryBase.delete(table="identity_group", id=id)
        except Exception as e:
            raise e



    @staticmethod
    def list() -> list:
        try:
            return RepositoryBase.list(
                table="identity_group",
                select="id, name, identity_group_identifier"
            )
        except Exception as e:
            raise e



    @staticmethod
    def add(data: dict) -> None:
        try:
            RepositoryBase.add(table="identity_group", data=data)
        except Exception as e:
            raise e
