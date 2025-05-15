from secops.models.Permission.Role import Role
from secops.models.Permission.IdentityGroup import IdentityGroup

from secops.models.Permission.repository.Permission import Permission as Repository
from secops.models.Permission.repository.PermissionPrivilege import PermissionPrivilege as PermissionPrivilegeRepository


class Permission:

    # IdentityGroupRole

    def __init__(self, permissionId: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id: int = int(permissionId)
        self.identityGroup: IdentityGroup
        self.role: Role

        self.__load()



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def delete(self) -> None:
        try:
            Repository.delete(self.id)
            del self
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def hasUserPermission(groups: list, action: str) -> bool:
        # Authorizations' fetch allowed for any (authenticated) user.
        if action == "authorizations_get":
            return True

        # Superadmin's group.
        for gr in groups:
            if gr.lower() == "automation.local":
                return True

        try:
            return bool(
                PermissionPrivilegeRepository.countUserPermissions(groups, action)
            )
        except Exception as e:
            raise e



    @staticmethod
    def permissionsDataList() -> list:
        # List of permissions as List[dict].
        try:
            return Repository.list()
        except Exception as e:
            raise e



    @staticmethod
    def authorizationsDataList(groups: list) -> list:
        # List of authorizations a user has, grouped by authorization type.
        superadmin = False
        for gr in groups:
            if gr.lower() == "automation.local":
                superadmin = True
                break

        if superadmin:
            # Superadmin's permissions override.
            authorizations = ["any"]
        else:
            try:
                authorizations = PermissionPrivilegeRepository.authorizationsList(groups)
            except Exception as e:
                raise e

        return authorizations



    @staticmethod
    def addFacade(identityGroupId: str, role: str) -> None:
        try:
            Permission.__add(
                identityGroup=IdentityGroup(identityGroupIdentifier=identityGroupId),
                role=Role(role=role)
            )
        except Exception as e:
            raise e



    @staticmethod
    def modifyFacade(permissionId: int, identityGroupId: str, role: str) -> None:
        try:
            Permission(permissionId).__modify(
                identityGroup=IdentityGroup(identityGroupIdentifier=identityGroupId),
                role=Role(role=role)
            )
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __load(self) -> None:
        try:
            info = Repository.get(self.id)

            self.identityGroup = IdentityGroup(id=info["id_group"])
            self.role = Role(id=info["id_role"])
        except Exception as e:
            raise e



    def __modify(self, identityGroup: IdentityGroup, role: Role) -> None:
        try:
            Repository.modify(
                self.id,
                identityGroupId=identityGroup.id,
                roleId=role.id
            )

            self.__load()
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private static methods
    ####################################################################################################################

    @staticmethod
    def __add(identityGroup: IdentityGroup, role: Role) -> None:
        try:
            Repository.add(
                identityGroupId=identityGroup.id,
                roleId=role.id
            )
        except Exception as e:
            raise e
