import io
import yaml
from typing import Callable
from kubernetes import config, client

from secops.helpers.Log import Log
from secops.helpers.Exception import CustomException


class KubernetesSupplicant:
    def __init__(self, asset: dict, silent: bool = False, **kwargs):
        self.silent = silent
        self.asset = asset

        # Using a file-like object instead of providing a .kube/config file in the filesystem.
        f = io.StringIO()
        f.write(yaml.dump({
            "apiVersion": "v1",
            "clusters": [
                {
                    "cluster": {
                        "certificate-authority-data": asset.get("certificateAuthorityData", ""),
                        "server": asset.get("baseurl", "")
                    },
                    "name": "default"
                }
            ],
            "contexts": [
                {
                    "context": {
                        "cluster": "default",
                        "namespace": "external-secrets",
                        "user": "default"
                    },
                    "name": "default"
                }
            ],
            "current-context": "default",
            "kind": "Config",
            "preferences": {},
            "users": [
                {
                    "name": "default",
                    "user": {
                        "client-certificate-data": asset.get("clientCertificateData", ""),
                        "client-key-data": asset.get("clientKeyData", "")
                    }
                }
            ]
        }))

        config.load_kube_config(config_file=f)



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    @staticmethod
    def perform(w: Callable, **kwargs):
        try:
            Log.actionLog("[Kubernetes Supplicant] Performing " + str(w))
            return w(**kwargs)
        except client.exceptions.ApiException as e:
            raise CustomException(status=e.status, payload={"Remote": e.__str__()})
        except Exception as e:
            raise e
