def events_for_pod(
    events: list[KubernetesEvent],
    pod_name: str,
) -> list[KubernetesEvent]:
    return [
        event
        for event in events
        if event.object_name == pod_name
    ]