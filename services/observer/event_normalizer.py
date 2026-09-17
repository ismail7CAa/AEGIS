from typing import Any
from packages.schemas.k8s_event import KubernetesEvent

def normalize_event(event: Any) -> KubernetesEvent:
    return KubernetesEvent(
        event_type=event.type,
        reason = event.reason,
        message=event.message, 
        object_name=event.involved_object.name,
        object_kind=event.involved_object.kind,
        count=event.count,
        first_timestamp=event.first_timestamp,
        last_timetamp=event.last_timestamp,

    )
def normalize_events(events:list[Any]) ->list[KubernetesEvent]:
    return[
        normalize_event(event)
        for event in events
    ]

def events_for_pod(
    events: list[KubernetesEvent],
    pod_name: str,
) -> list[KubernetesEvent]:
    return [
        event
        for event in events
        if event.object_name == pod_name
    ]