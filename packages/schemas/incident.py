from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class IncidentType(str, Enum):
    OOM_KILLED = "oom_killed"
    CRASH_LOOP  = "crash_loop"
    READINESS_FAILURE = "readiness_failure"

class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Incident(BaseModel):
    incident_type: IncidentType
    severity: Severity
    namespace: str
    pod: str
    container: str
    reason: str | None = None
    exit_code: int | None = None
    restart_count: int = 0
    detected_at: datetime
    