import os

from packages.k8s_clients.client import KubernetesClient
from services.detector.detector import detect_incidents
from services.observer.normalizer import normalize_pod


def main() -> None:
    namespace = os.getenv("AEGIS_NAMESPECE", "aegis-lab")

    kube = KubernetesClient()
    pods = kube.list_pods(namespace)

    print("\nAEGIS Observer")
    print(f"Namespace: {namespace}")
    print(f"Pods discovered: {len(pods)}")
    print("-" * 70)

    for pod in pods:
        state = normalize_pod(pod)

        incidents = detect_incidents(state)
        for incident in incidents:
            print(incident.model_dump_json(indent = 2))
        print(state.model_dump_json(indent=2))
        print("-" * 70)

if __name__ == "__main__":
    main()