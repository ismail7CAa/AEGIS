from datetime import datetime
from pydantic import BaseModel

class KubernetesEvent(BaseModel):
    event_type: str | None
    reason: str | None
    message: str | None

    object_name: str | None
    object_kind: str | None

    count: int | None = None

    first_timetamp: datetime | None = None
    last_timetamp: datetime | None = None 