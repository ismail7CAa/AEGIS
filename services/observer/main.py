import os 

from kubernetes.client import V1ContainerStatus, V1Pod

from packages.k8s_clients.client import kubernetesClient
from packages.schemas.pod_state import ContainerState, PodState

def normalize_container(status: V1ContainerStatus) -> ContainerState:
    """
    Convert Kubernetes container status into our internal AEGIS schema.
    """

    waiting_reason: str | None = None
    terminated_reason: str | None = None
    exist_code: int | None = None

     # Current state: e.g. CrashLoopBAckOff
    if status.state and status.state.waiting:
        waiting_reason = status.state.waiting.reason
    # Container might currently be terminated
    if status.state and status.state.terminated:
        terminated_reason = status.state.terminated.reason
        exist_code = status.state.terminated.exit_code
    # Or K8s may already have restarted yet
    # This is especially important for OOMKilled
    elif status.last_state and status.last_state.terminated:
        terminated_reason = status.last_state.terminated.reason
        exist_code = status.last_state.terminated.exit_code

    return ContainerState(
        name=status.name,
        ready=status.ready,
        restart_count=status.restart_count,
        waiting_reason=waiting_reason,
        terminated_reason=terminated_reason,
        exit_code=exist_code
    )

def normalize_pod(pod: V1Pod) -> PodState:
    """
    Convert a raw Kubernetes pod object into our AEGIS PodState.
    """
    containers = []
    if pod.status.container_statuses:
        containers = [
            normalize_container(status) for status in pod.status.container_statuses 
        ]

    return PodState(
        namespace=pod.metadata.namespace,
        name=pod.metadata.name,
        phase=pod.status.phase,
        containers=containers
    )
def main() -> None:
    namespace = os.getenv("AEGIS_NAMESPECE", "aegis-lab")

    kube = kubernetesClient()
    pods = kube.list_pods(namespace)

    print(f"\nAEGIS Observer")
    print(f"Namespace: {namespace}")
    print(f"Pods discovered: {len(pods)}")
    print("-" * 70)

    for pod in pods:
        state = normalize_pod(pod)

        print(state.model_dump_json(indent=2))
        print("-" * 70)

if __name__ == "__main__":
    main()