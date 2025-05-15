from __future__ import annotations

from secops.models.CyberArk.Account import Account

from secops.models.CyberArk.backend.Safe import Safe as Backend

from secops.helpers.Misc import Misc


class Safe:
    def __init__(self, asset: dict, id: str, **kwargs):
        self.asset = asset

        self.safeUrlId: str = id
        self.safeName: str = ""
        self.safeNumber: int = 0
        self.location: str = ""
        self.creator: dict = {}
        self.olacEnabled: bool = False
        self.numberOfVersionsRetention: object = None
        self.numberOfDaysRetention: int = 0
        self.autoPurgeEnabled: bool = False
        self.creationTime: int = 0
        self.lastModificationTime: int = 0
        self.description: str = ""
        self.managingCPM: str = ""
        self.isExpiredMember: bool = False

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
            Backend.modify(self.asset, self.safeUrlId, data, **self.kwargs)

            for k, v in Misc.toDict(data).items():
                setattr(self, k, v)
        except Exception as e:
            raise e



    def delete(self) -> None:
        try:
            Backend.delete(self.asset, self.safeUrlId, **self.kwargs)
            del self
        except Exception as e:
            raise e



    def membersRawDataList(self) -> list:
        try:
            return Backend.members(self.asset, self.safeUrlId, **self.kwargs)
        except Exception as e:
            raise e



    def addMember(self, data: dict) -> dict:
        try:
            o = Backend.addMember(self.asset, self.safeUrlId, data, **self.kwargs)
            for k, v in Misc.toDict(data).items():
                setattr(self, k, v)

            return o
        except Exception as e:
            raise e



    def accountsRawDataList(self) -> list:
        try:
            return Account.rawDataList(self.asset, self.safeUrlId, **self.kwargs)
        except Exception as e:
            raise e



    def addAccount(self, data: dict) -> dict:
        try:
            o = Backend.addAccount(self.asset, self.safeName, data, **self.kwargs)
            for k, v in Misc.toDict(data).items():
                setattr(self, k, v)

            return o
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def rawDataList(**kwargs) -> list:
        try:
            return Backend.list(**kwargs)
        except Exception as e:
            raise e



    @staticmethod
    def add(**kwargs) -> None:
        try:
            Backend.add(**kwargs)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __load(self, **kwargs) -> None:
        try:
            info = Backend.get(self.asset, self.safeUrlId, **kwargs)

            # Set attributes.
            for k, v in info.items():
                setattr(self, k, v)
        except Exception as e:
            raise e
