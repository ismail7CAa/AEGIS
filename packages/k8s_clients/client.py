from typing import Any, cast

from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException


class KubernetesClient:
    def __init__(self) -> None:
        self._load_config()
        self.core = client.CoreV1Api()

    @staticmethod
    def _load_config() -> None:
        try:
            config.load_incluster_config()
        except ConfigException:
            config.load_kube_config()

    def list_pods(self, namespace: str) -> list[Any]:
        result = self.core.list_namespaced_pod(namespace)
        return cast(list[Any], result.items)

    def list_events(self, namespace: str) -> list[Any]:
        result = self.core.list_namespaced_event(namespace)
        return cast(list[Any], result.items)