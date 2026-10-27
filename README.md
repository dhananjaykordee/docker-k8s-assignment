# Docker and Kubernetes Deployment

This guide documents the Docker and Kubernetes work for the Meeting Room
Booking application. It covers building the app image, deploying it to
Docker Desktop Kubernetes, installing Traefik and NGINX with Helm, routing
traffic through an Ingress, and checking the running resources.

## Repository structure

```text
meeting-room-booking/
├── README.md
├── Dockerfile
├── app.py
├── configmap.yaml
├── deployment.yaml
├── ingress.yaml
├── service.yaml
├── requirements.txt
├── rooms.json
├── Assignment_Report.md
├── screenshot/
│   └── Screenshots/
├── auth/
├── model/
├── repository/
├── routes/
├── services/
├── tests/
└── utils/
```

This repository contains a FastAPI application, so it does not currently have
an `index.html` frontend. The assignment report is `Assignment_Report.md`
rather than a PDF.

## Prerequisites

- Docker Desktop for Windows with the Docker Engine running.
- Kubernetes enabled in Docker Desktop.
- `kubectl` configured to use the Docker Desktop cluster.
- Helm installed.
- PowerShell.

Install Docker Desktop using the
[official Windows installation guide](https://docs.docker.com/desktop/setup/install/windows-install/).
Verify the tools and cluster:

```powershell
docker --version
kubectl config current-context
kubectl get nodes
helm version
```

The Kubernetes node should report `Ready`.

## Build the application image

Run these commands from the `meeting-room-booking` directory. The image tag
must match the image configured in `deployment.yaml`:

```powershell
docker build -t docker-demo:v1 .
docker image inspect docker-demo:v1
```

Docker Desktop Kubernetes can use images built locally by Docker Desktop.

## Install Traefik with Helm

Traefik is the Ingress controller. It receives HTTP requests and routes them
to Kubernetes Services according to Ingress rules.

```powershell
helm repo add traefik https://traefik.github.io/charts
helm repo update
helm upgrade --install traefik traefik/traefik `
  --namespace traefik --create-namespace
kubectl get pods,services -n traefik
```

## Deploy the application to Kubernetes

The app uses an embedded H2 database, so it does not need database credentials.
It does need a JWT signing secret. Generate one and store it as a Kubernetes
Secret; do not commit the generated value:

```powershell
$jwtSecret = python -c "import secrets; print(secrets.token_urlsafe(32))"
kubectl create secret generic meeting-room-booking-secrets `
  --from-literal="secret-key=$jwtSecret"
```

Apply the ConfigMap, Services, StatefulSet, and Ingress manifests:

```powershell
kubectl apply -f configmap.yaml
kubectl apply -f service.yaml
kubectl apply -f deployment.yaml
kubectl apply -f ingress.yaml
kubectl rollout status statefulset/docker-demo
```

Inspect the resources:

```powershell
kubectl get statefulset,pods,services,ingress,pvc
kubectl describe ingress meeting-room
kubectl describe pod <pod-name>
```

The `docker-demo` StatefulSet is configured with two replicas using the
`docker-demo:v1` image. Each pod requests a separate 1 GiB persistent volume
claim mounted at `/app/data`. A pod replacement can reuse its claim, but the
two replicas have separate H2 database files and do not share booking data.

## Access through Ingress

The Ingress rule uses host `localhost` and sends traffic to the `docker-demo`
ClusterIP Service on port `80`:

```text
Browser -> Traefik Ingress Controller -> meeting-room Ingress
        -> docker-demo Service -> application pod
```

Open the application through the local Ingress at:

```text
http://localhost/
```

The Ingress serves port `80`. Alternatively, to use local port `8080`, start a
port-forward and leave the terminal running:

```powershell
kubectl port-forward service/docker-demo 8080:80
```

Then connect to `http://localhost:8080/`. The port-forward stops when its
command is stopped or its terminal closes.

## Optionally deploy NGINX with Helm

This installs NGINX as a separate web server. It does not replace Traefik as
the Ingress controller:

```powershell
helm upgrade --install nginx `
  oci://registry-1.docker.io/bitnamicharts/nginx `
  --namespace default
kubectl get pods,services -n default
```

To route the existing `localhost` Ingress to NGINX, change the Ingress backend
Service name in `ingress.yaml` to `nginx` and apply it:

```powershell
kubectl apply -f ingress.yaml
```

To route back to the Meeting Room application, set the backend Service name to
`docker-demo` and apply the manifest again. The Ingress and backend Service
must be in the same namespace.

## Docker and Kubernetes screenshots

The Docker screenshot shows an NGINX container running with a host port
mapping. The Kubernetes screenshot shows a successful workload rollout.

![Docker container and port mapping](<screenshot/Screenshots/Screenshot 2026-10-26 164016.png>)

![Kubernetes workload rollout](<screenshot/Screenshots/Screenshot 2026-10-27 114931.png>)

## Cleanup

Remove the application workloads and related resources while keeping the
database PVCs:

```powershell
kubectl delete statefulset docker-demo
kubectl delete ingress meeting-room
kubectl delete service docker-demo docker-demo-headless
kubectl delete configmap meeting-room-booking-config
kubectl delete secret meeting-room-booking-secrets
```

Check PVCs before deleting them. Deleting a PVC may delete its stored H2 data,
depending on the cluster's storage configuration:

```powershell
kubectl get pvc
```

Uninstall the Helm releases when they are no longer needed:

```powershell
helm uninstall nginx -n default
helm uninstall traefik -n traefik
```
