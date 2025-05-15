from __future__ import annotations

from secops.models.Kubernetes.backend.Secret import Secret as Backend

from secops.helpers.Misc import Misc


class Secret:
    def __init__(self, asset: dict, name: str, namespace: str, **kwargs):
        self.asset: dict = asset
        self.name: str = name
        self.namespace: str = namespace

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
            info = Backend.get(self.asset, name=self.name, namespace=self.namespace, **kwargs)

            # Set attributes.
            for k, v in info.items():
                setattr(self, k, v)
        except Exception as e:
            raise e
