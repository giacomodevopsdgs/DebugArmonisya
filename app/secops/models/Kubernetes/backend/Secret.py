from kubernetes import client

from secops.helpers.KubernetesSupplicant import KubernetesSupplicant
from secops.helpers.Exception import CustomException


class Secret:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def get(asset: dict, name: str, namespace: str, **kwargs) -> dict:
        try:
            KubernetesSupplicant(asset=asset)
            return KubernetesSupplicant.perform(
                w=client.CoreV1Api().read_namespaced_secret,
                name=name,
                namespace=namespace
            )
        except Exception as e:
            raise e



    @staticmethod
    def add(asset: dict, name: str, namespace: str, data: dict, **kwargs) -> None:
        try:
            secret = client.V1Secret(
                metadata=client.V1ObjectMeta(
                    name=name,
                    annotations={
                        "managed_by": "Armonisya"
                    },
                ),
                data=data
            )

            try:
                KubernetesSupplicant(asset=asset)
                KubernetesSupplicant.perform(
                    w=client.CoreV1Api().create_namespaced_secret,
                    namespace=namespace,
                    body=secret
                )
            except CustomException as e:
                if e.status == 409:
                    try:
                        KubernetesSupplicant.perform(
                            w=client.CoreV1Api().replace_namespaced_secret,
                            name=name,
                            namespace=namespace,
                            body=secret
                        )
                    except Exception as e:
                        raise e
                else:
                    raise e
        except Exception as e:
            raise e
