from packages.k8s_clients.client import KubernetesClient

def main() -> None:
    kube = KubernetesClient()

    namespace = "aegis-lab"
    pods = kube.list_pods(namespace)

    for pod in pods:
        if not pod.metadata.name.startswith("crash-lab"):
            continue
        pod_name = pod.metadata.name

        if not pod.status.container_statuses:
            continue

        container_name= pod.status.container_statuses[0].name

        print(f"Pod: {pod_name}")
        print(f"Container: {container_name}")

        print("\n--- CURRENT LOGS ---")

        current_logs = kube.get_pod_logs(
            namespace=namespace,
            pod_name=pod_name,
            container_name=container_name,
        )
        print(current_logs)

        print("\n--- PREVIOUS LOGS ---")

        previous_logs = kube.get_pod_logs(
            namespace=namespace,
            pod_name=pod_name,
            container_name=container_name,
            previous=True,
        )
        print(previous_logs)

if __name__== "__main__":
    main()