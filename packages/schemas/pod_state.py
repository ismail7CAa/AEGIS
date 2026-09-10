from pydantic import BaseModel

class ContainerState(BaseModel):
    name: str
    ready: bool
    restart_count: int
    waiting_reason: str | None = None
    terminated_reason: str | None = None
    exist_code: int | None = None

class PodState(BaseModel):
    namespace: str
    name: str
    phase: str
    node: str | None = None

    containers: list[ContainerState]
    