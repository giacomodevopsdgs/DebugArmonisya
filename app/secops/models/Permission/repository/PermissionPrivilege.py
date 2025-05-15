from typing import List, Dict

from django.db import connection

from secops.helpers.Exception import CustomException
from secops.helpers.Database import Database as DBHelper


class PermissionPrivilege:

    # Tables: group_role, identity_group, role, privilege

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(filterGroups: list = None, showPrivileges: bool = False) -> list:
        # List identity groups with related information regarding the associated roles,
        # and optionally detailed privileges' descriptions.
        filterGroups = filterGroups or []
        groupWhere = ""
        j = 0

        c = connection.cursor()

        try:
            # Build WHERE clause when filterGroups is specified.
            if filterGroups:
                groupWhere = "WHERE ("
                for _ in filterGroups:
                    groupWhere += "identity_group.identity_group_identifier = %s || "
                groupWhere = groupWhere[:-4] + ") "

            c.execute(
                "SELECT identity_group.*, " 

                "IFNULL(GROUP_CONCAT( "
                    "DISTINCT role.role " 
                    "ORDER BY role.id "
                    "SEPARATOR ',' "
                "), '') AS roles, "

                "IFNULL(GROUP_CONCAT( "
                    "DISTINCT privilege.privilege " 
                    "ORDER BY privilege.id "
                    "SEPARATOR ',' "
                "), '') AS privileges "

                "FROM identity_group "
                "LEFT JOIN group_role ON group_role.id_group = identity_group.id "
                "LEFT JOIN role ON role.id = group_role.id_role "
                "LEFT JOIN role_privilege ON role_privilege.id_role = role.id "
                "LEFT JOIN privilege ON privilege.id = role_privilege.id_privilege "
                + groupWhere +
                "GROUP BY identity_group.id",
                      filterGroups
            )

            items: List[Dict] = DBHelper.asDict(c)
            for ln in items:
                if "roles" in items[j]:
                    if "," in ln["roles"]:
                        items[j]["roles"] = ln["roles"].split(",")
                    else:
                        items[j]["roles"] = [ ln["roles"] ]

                if showPrivileges:
                    if "privileges" in items[j]:
                        if "," in ln["privileges"]:
                            items[j]["privileges"] = ln["privileges"].split(",")
                        else:
                            items[j]["privileges"] = [ln["privileges"]]
                else:
                    del items[j]["privileges"]

                j = j+1

            return items
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def authorizationsList(groups: list) -> list:
        permissions = list()

        try:
            o = PermissionPrivilege.list(filterGroups=groups, showPrivileges=True)

            # Collect every permission related to the group in groups.
            for identityGroup in groups:
                for el in o:
                    if "identity_group_identifier" in el:
                        if el["identity_group_identifier"].lower() == identityGroup.lower():
                            permissions.append(el["privileges"])
        except Exception as e:
            raise e

        return permissions



    @staticmethod
    def countUserPermissions(groups: list, action: str) -> int:
        if action and groups:
            args = groups.copy()
            groupWhere = ""

            c = connection.cursor()

            try:
                for _ in groups:
                    groupWhere += "identity_group.identity_group_identifier = %s || " # identity_group.identity_group_identifier = %s || identity_group.identity_group_identifier = %s || ...

                args.append(action)

                c.execute(
                    "SELECT COUNT(*) AS count "
                    "FROM identity_group "
                    "LEFT JOIN group_role ON group_role.id_group = identity_group.id "
                    "LEFT JOIN role ON role.id = group_role.id_role "
                    "LEFT JOIN role_privilege ON role_privilege.id_role = role.id "
                    "LEFT JOIN privilege ON privilege.id = role_privilege.id_privilege "
                    "WHERE (" + groupWhere[:-4] + ") " +
                    "AND privilege.privilege = %s ",
                        args
                )

                return DBHelper.asDict(c)[0]["count"]
            except Exception as e:
                raise CustomException(status=400, payload={"database": e.__str__()})
            finally:
                c.close()

        return 0
