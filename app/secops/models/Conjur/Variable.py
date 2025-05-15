from __future__ import annotations

from secops.models.Conjur.backend.Variable import Variable as Backend

from secops.helpers.Misc import Misc


class Variable:
    def __init__(self, asset: dict, id: str, **kwargs):
        self.asset = asset
        self.id: str = id
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



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def rawDataList(asset: dict, noCache: bool = False, **kwargs) -> list:
        try:
            return Backend.list(resource="variable", asset=asset, noCache=noCache, **kwargs)
        except Exception as e:
            raise e



    def addSecret(self, data: dict) -> None:
        try:
            Backend.addSecret(self.asset, self.id, data=data, **self.kwargs)

            for k, v in Misc.toDict(data).items():
                setattr(self, k, v)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __load(self, **kwargs) -> None:
        try:
            info = Backend.get(resource="variable", asset=self.asset, id=self.id, **kwargs)

            # Set attributes.
            for k, v in info.items():
                setattr(self, k, v)
        except Exception as e:
            raise e
