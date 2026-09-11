from datetime import UTC, datetime

from packages.schemas.incident import Incident, IncidentType, Severity
from packages.schemas.pod_state import PodState


def detect_incidents(pod: PodState) -> list[Incident]:
    incidents: list[Incident] = []
    for container in pod.containers:
        if container.terminated_reason == "OOMKilled" :
            incidents.append(
                Incident(
                    incident_type = IncidentType.OOM_KILLED,
                    severity = Severity.HIGH,
                    namespace = pod.namespace,
                    pod = pod.name,
                    container = container.name,
                    reason = container.terminated_reason,
                    exit_code = container.exit_code,
                    restart_count = container.restart_count,
                    detected_at = datetime.now(UTC),
                
                )
            )
        elif (
            container.waiting_reason == "CrashLoopBackOff"
            or (
                container.restart_count >= 2
                and container.exit_code is not None
                and container.exit_code != 0
            )
        ):
            incidents.append(
                Incident(
                    incident_type = IncidentType.CRASH_LOOP,
                    severity = Severity.HIGH,
                    namespace = pod.namespace,
                    pod = pod.name,
                    container = container.name,
                    reason = container.waiting_reason
                    or container.terminated_reason,
                    exit_code = container.exit_code,
                    restart_count = container.restart_count,
                    detected_at = datetime.now(UTC),
                )
            )
        elif pod.phase == "Running" and not container.ready:
            incidents.append(
                Incident(
                    incident_type = IncidentType.READINESS_FAILURE,
                    severity = Severity.MEDIUM,
                    namespace = pod.namespace,
                    pod = pod.name,
                    container = container.name,
                    reason = "Container is running but not ready",
                    restart_count = container.restart_count,
                    detected_at = datetime.now(UTC),

                )
            )
    return incidents
