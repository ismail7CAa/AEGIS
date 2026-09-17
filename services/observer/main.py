import os

from packages.k8s_clients.client import KubernetesClient
from services.detector.detector import detect_incidents
from services.observer.normalizer import normalize_pod
from services.observer.event_normalizer import (
    events_for_pod,
    normalize_events,
)

def main() -> None:
    namespace = os.getenv("AEGIS_NAMESPECE", "aegis-lab")

    kube = KubernetesClient()
    pods = kube.list_pods(namespace)

    raw_events = kube.list_events(namespace)
    events=normalize_events(raw_events)

    print("\nAEGIS Observer")
    print(f"Namespace: {namespace}")
    print(f"Pods discovered: {len(pods)}")
    print("-" * 70)

    for pod in pods:
        state = normalize_pod(pod)
        pod_events = events_for_pod(
            events,
            state.name,
        )
        incidents = detect_incidents(state)

        for incident in incidents:
            current_logs = kube.get_pod_logs(
                namespace=incident.namespace,
                pod_name=incident.pod,
                container= incident.container,
                previous=False,
            )

            previous_logs = kube.get_pod_logs(
                namespace=incident.namespace,
                pod_name=incident.pod,
                container= incident.container,
                previous=True,
            )
            print(incident.model_dump_json(indent = 2))

            print("\nCurrent logs:")
            print(current_logs)

            print("\nPrevious logs:")
            print(previous_logs)

            print("\nKubernetes Events:")
            for event in pod_events:
                print (
                    f"-[{event.event_type}]"
                    f"{event.reason}"
                    f"{event.message}"
                )
        print(state.model_dump_json(indent=2))
        print("-" * 70)

if __name__ == "__main__":
    main()