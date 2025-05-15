from __future__ import annotations

from secops.models.Kubernetes.backend.Pod import Pod as Backend


class Pod:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def rawDataList(asset: dict, **kwargs) -> list:
        try:
            return Backend.list(asset=asset, **kwargs)
        except Exception as e:
            raise e
