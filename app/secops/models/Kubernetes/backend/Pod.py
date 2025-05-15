from kubernetes import client

from secops.helpers.KubernetesSupplicant import KubernetesSupplicant


class Pod:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(asset: dict, **kwargs) -> list:
        pods = []

        try:
            KubernetesSupplicant(asset=asset)
            l = KubernetesSupplicant.perform(client.CoreV1Api().list_pod_for_all_namespaces)
            for i in l.items:
                pods.append({
                    "ip": i.status.pod_ip,
                    "namespace": i.metadata.namespace,
                    "name": i.metadata.name
                })

            return pods
        except Exception as e:
            raise e
