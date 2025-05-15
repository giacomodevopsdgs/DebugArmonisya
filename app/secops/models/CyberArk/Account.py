from __future__ import annotations

from secops.models.CyberArk.backend.Account import Account as Backend

from secops.helpers.Misc import Misc


class Account:
    def __init__(self, asset: dict, id: str, **kwargs):
        self.asset = asset

        self.id: str = id
        self.safeName: str = ""
        self.name: str = ""
        self.address: str = ""
        self.secretType: str = ""
        self.userName: str = ""
        self.secret: str = ""
        self.categoryModificationTime: int = 0
        self.createdTime: int = 0
        self.secretManagement: dict = {}
        self.platformId: str = ""
        self.platformAccountProperties: dict = {}

        self.kwargs = kwargs

        self.__load(**kwargs)



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def repr(self):
        o = Misc.deepRepr(self)
        del o["kwargs"]
        del o["asset"]

        return o



    def modify(self, data: dict) -> None:
        try:
            Backend.modify(self.asset, self.id, data, **self.kwargs)

            for k, v in Misc.toDict(data).items():
                setattr(self, k, v)
        except Exception as e:
            raise e



    def delete(self) -> None:
        try:
            Backend.delete(self.asset, self.id, **self.kwargs)
            del self
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def rawDataList(asset: dict, safeName: str = "", noCache: bool = False, **kwargs) -> list:
        try:
            return Backend.list(asset, safeName=safeName, noCache=noCache, **kwargs)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __load(self, **kwargs) -> None:
        try:
            info = Backend.get(self.asset, self.id, **kwargs)

            # Set attributes.
            for k, v in info.items():
                setattr(self, k, v)
        except Exception as e:
            raise e
