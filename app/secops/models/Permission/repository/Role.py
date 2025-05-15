from secops.helpers.RepositoryBase import RepositoryBase


class Role:

    # Table: role

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def get(id: int, role: str) -> dict:
        where = []
        if id:
            where = [("id", id, "int")]
        if role:
            where = [("role", role, "string")]

        try:
            return RepositoryBase.get(
                table="role",
                select="id, role, IFNULL(description, '') AS description",
                where=where
            )
        except Exception as e:
            raise e



    @staticmethod
    def list() -> list:
        try:
            return RepositoryBase.list(
                table="role",
                select="id, role, IFNULL(description, '') AS description"
            )
        except Exception as e:
            raise e
