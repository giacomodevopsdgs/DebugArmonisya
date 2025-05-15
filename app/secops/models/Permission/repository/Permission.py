from secops.helpers.RepositoryBase import RepositoryBase


class Permission:

    # IdentityGroupRole

    # Tables: group_role, identity_group, role

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def get(permissionId: int) -> dict:
        try:
            return RepositoryBase.get(
                table="group_role",
                select="*",
                where=[("id", permissionId, "int")]
            )
        except Exception as e:
            raise e



    @staticmethod
    def modify(permissionId: int, identityGroupId: int, roleId: int) -> None:
        try:
            RepositoryBase.modify(table="group_role", id=permissionId, data={
                "id_group": identityGroupId,
                "id_role": roleId
            })
        except Exception as e:
            raise e



    @staticmethod
    def delete(permissionId: int) -> None:
        try:
            return RepositoryBase.delete(table="group_role", id=permissionId)
        except Exception as e:
            raise e



    @staticmethod
    def list() -> list:
        from django.db import connection

        from secops.helpers.Exception import CustomException
        from secops.helpers.Database import Database as DBHelper

        c = connection.cursor()

        try:
            c.execute(
                "SELECT "
                    "group_role.id, "
                    "identity_group.name AS identity_group_name, "
                    "identity_group.identity_group_identifier AS identity_group_identifier, "
                    "role.role AS role "
                "FROM identity_group "
                "LEFT JOIN group_role ON group_role.id_group = identity_group.id "
                "LEFT JOIN role ON role.id = group_role.id_role "
                "WHERE role.role IS NOT NULL")
            return DBHelper.asDict(c)
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def add(identityGroupId: int, roleId: int) -> None:
        try:
            RepositoryBase.add(table="group_role", data={
                "id_group": identityGroupId,
                "id_role": roleId
            })
        except Exception as e:
            raise e
