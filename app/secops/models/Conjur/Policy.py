from __future__ import annotations

from secops.models.Conjur.backend.Policy import Policy as Backend

from secops.helpers.Misc import Misc


class Policy:
    def __init__(self, resource: str, asset: dict, id: str, **kwargs):
        self.asset = asset
        self.id: str = id
        self.kwargs = kwargs

        self.__load(resource, **kwargs)



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
    def rawDataList(resource: str, asset: dict, noCache: bool = False, **kwargs) -> list:
        try:
            return Backend.list(resource=resource, asset=asset, noCache=noCache, **kwargs)
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

    def __load(self, resource, **kwargs) -> None:
        try:
            info = Backend.get(resource=resource, asset=self.asset, id=self.id, **kwargs)

            # Set attributes.
            for k, v in info.items():
                setattr(self, k, v)
        except Exception as e:
            raise e
