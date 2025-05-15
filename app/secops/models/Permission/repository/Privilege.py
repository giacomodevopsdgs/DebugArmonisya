from secops.helpers.RepositoryBase import RepositoryBase


class Privilege:

    # Table: privilege

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def get(id: int) -> dict:
        try:
            return RepositoryBase.get(
                table="privilege",
                select="id, privilege, IFNULL(description, '') AS description",
                where=[("id", id, "int")]
            )
        except Exception as e:
            raise e



    @staticmethod
    def list() -> list:
        try:
            return RepositoryBase.list(
                table="privilege",
                select="id, privilege, IFNULL(description, '') AS description"
            )
        except Exception as e:
            raise e
