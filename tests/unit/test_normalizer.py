from kubernetes.client import (
    V1ContainerState,
    V1ContainerStateTerminated,
    V1ContainerStateWaiting,
    V1ContainerStatus,
)

from services.observer.normalizer import normalize_container


def test_normalizer_container_oomkilled():
    status = V1ContainerStatus(
        name = "memory-hog",
        ready = False,
        restart_count = 3,
        image = "test", 
        image_id = "test",
        container_id = "test",
        state = V1ContainerState(),
        last_state = V1ContainerState(
            terminated = V1ContainerStateTerminated(
                exit_code = 137,
                reason = "OOMKilled",
            )
        ),
    )
    result = normalize_container(status)

    assert result.name == "memory-hog"
    assert result.ready is False
    assert result.restart_count == 3
    assert result.terminated_reason == "OOMKilled"
    assert result.exit_code == 137

def test_normalize_container_crashloop():
    status = V1ContainerStatus(
        name = "crashing-app",
        ready= False,
        restart_count= 5,
        image = "test",
        image_id = "test",
        container_id = "test",
        state = V1ContainerState(
            waiting= V1ContainerStateWaiting(
                reason = "CrashLoopBackOff"
            )
        ),
        last_state = V1ContainerState(
            terminated = V1ContainerStateTerminated(
                exit_code = 1,
                reason = "Error",
            )
        ),
    )
    result = normalize_container(status)

    assert result.waiting_reason == "CrashLoopBackOff"
    assert result.terminated_reason == "Error"
    assert result.exit_code == 1
    assert result.restart_count == 5

def test_normalize_healthy_container():
    status = V1ContainerStatus(
        name = "lab-api",
        ready = True,
        restart_count = 0,
        image = "test",
        image_id = "test",
        container_id = "test",
        state = V1ContainerState(),
        last_state = V1ContainerState(),
    )

    result = normalize_container(status)

    assert result.ready is True
    assert result.restart_count == 0
    assert result.waiting_reason is None
    assert result.terminated_reason is None
    assert result.exit_code is None