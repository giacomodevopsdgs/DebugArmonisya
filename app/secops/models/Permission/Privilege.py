from __future__ import annotations
from typing import List

from secops.models.Permission.repository.Privilege import Privilege as Repository


class Privilege:
    def __init__(self, id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id: int = int(id)
        self.privilege: str = ""
        self.description: str = ""

        self.__load()



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def repr(self):
        return repr(self)



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list() -> List[Privilege]:
        privileges = []

        try:
            for privilege in Repository.list():
                privileges.append(
                    Privilege(privilege["id"])
                )

            return privileges
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __load(self) -> None:
        try:
            info = Repository.get(self.id)

            # Set attributes.
            for k, v in info.items():
                setattr(self, k, v)
        except Exception as e:
            raise e
