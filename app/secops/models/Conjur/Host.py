from __future__ import annotations

from secops.models.Conjur.backend.Host import Host as Backend

from secops.helpers.Misc import Misc


class Host:
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
            return Backend.list(resource="host", asset=asset, noCache=noCache, **kwargs)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __load(self, **kwargs) -> None:
        try:
            info = Backend.get(resource="host", asset=self.asset, id=self.id, **kwargs)

            # Set attributes.
            for k, v in info.items():
                setattr(self, k, v)
        except Exception as e:
            raise e
