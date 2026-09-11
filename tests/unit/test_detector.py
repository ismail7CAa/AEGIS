from packages.schemas.incident import IncidentType
from packages.schemas.pod_state import ContainerState, PodState
from services.detector.detector import detect_incidents


def test_detect_oom_killed():
    pod = PodState(
        namespace = "aegis-lab",
        name = "oom-test",
        phase = "Running",
        node = "worker-1",
        containers = [
            ContainerState(
                name = "memory-hog",
                ready = False,
                restart_count = 5,
                waiting_reason = "CrashLoopBackOff",
                terminated_reason = "OOMKilled",
                exit_code = 137,
            )
        ],
    )
    incidents = detect_incidents(pod)

    assert len(incidents) == 1
    assert incidents[0].incident_type == IncidentType.OOM_KILLED
    assert incidents[0].exit_code == 137

def test_detect_crash_loop():
    pod = PodState(
        namespace = "aegis-lab",
        name = "crash-test",
        phase = "Running",
        node = "worker-1",
        containers = [
            ContainerState(
                name = "crashing-app",
                ready = False,
                restart_count = 7,
                waiting_reason = "CrashLoopBackOff",
                terminated_reason = "Error",
                exit_code = 1,

            )
        ],
    )
    incidents = detect_incidents(pod)

    assert len(incidents) == 1
    assert incidents[0].incident_type == IncidentType.CRASH_LOOP
    assert incidents[0].exit_code == 1 
    assert incidents[0].restart_count == 7

def test_healthy_pod_has_no_incident():
    pod = PodState(
        namespace = "aegis-lab",
        name = "healthy-api",
        phase = "Running",
        node = "worker-1",
        containers = [
            ContainerState(
                name = "lab-api",
                ready = True,
                restart_count = 0,
                waiting_reason = None,
                terminated_reason = None,
                exit_code = None,
            )
        ],
    )
    incidents = detect_incidents(pod)

    assert incidents == []

def test_multi_container_pod_detects_only_broken_container():
    pod = PodState(
        namespace = "aegis-lab",
        name = "multi-container-test",
        phase = "Running",
        node = "worker-1",
        containers = [
            ContainerState(
                name = "healthy-sidecar",
                ready = True,
                restart_count = 0,
                waiting_reason = None,
                terminated_reason = None,
                exit_code = None,
            
            ),
            ContainerState(
                name = "broken-app",
                ready = False,
                restart_count = 4,
                waiting_reason = "CrashLoopBackOff",
                terminated_reason = "Error",
                exit_code = 1,
            ),
        ],
    )
    incidents = detect_incidents(pod)

    assert len(incidents) == 1

    incident = incidents[0]
    assert incident.incident_type == IncidentType.CRASH_LOOP
    assert incident.container == "broken-app"
    assert incident.exit_code == 1