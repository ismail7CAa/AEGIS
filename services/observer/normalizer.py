from kubernetes.client import V1ContainerStatus, V1Pod

from packages.schemas.pod_state import ContainerState, PodState


def normalize_container(status: V1ContainerStatus) -> ContainerState:
    waiting_reason: str | None = None
    terminated_reason: str | None = None
    exit_code: int | None = None

    # Current waiting state
    if status.state and status.state.waiting:
        waiting_reason = status.state.waiting.reason

    # Current terminated state
    if status.state and status.state.terminated:
        terminated_reason = status.state.terminated.reason
        exit_code = status.state.terminated.exit_code

    # Previous terminated state
    if status.last_state and status.last_state.terminated:
        terminated_reason = status.last_state.terminated.reason
        exit_code = status.last_state.terminated.exit_code

    return ContainerState(
        name=status.name,
        ready=status.ready,
        restart_count=status.restart_count,
        waiting_reason=waiting_reason,
        terminated_reason=terminated_reason,
        exit_code=exit_code,
    )

def normalize_pod(pod: V1Pod) -> PodState:
    containers = []

    if pod.status.container_statuses:
        containers = [
            normalize_container(status)
            for status in pod.status.container_statuses
        ]
    return PodState(
        namespace = pod.metadata.namespace,
        name = pod.metadata.name,
        phase = pod.status.phase,
        node = pod.spec.node_name,
        containers = containers,
    )