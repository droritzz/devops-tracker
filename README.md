# DevOps Tracker. Project Milestones

### Milestone 1: Core App (Local)

Goal: Have a working app + DB locally.

Features:
1. User can add a project (e.g., “DevOps Learning”).
2. Add milestones (title, description, status: Todo/In Progress/Done).
3. View progress dashboard

Stack:
1. Backend: FastAPI (Python) or Express.js (Node).
2. DB: PostgreSQL (via docker-compose).
3. Frontend: Simple React.

Deliverable: App runs with docker-compose up.

### Milestone 2: Containerization

Goal: Run the app in Docker.

1. Write Dockerfile for backend + frontend.
2. Update docker-compose.yml to use images.
3. Test locally with containers only.

### Milesetone 3: CI/CD with GitHub Action

Goal: Automated builds & pushes.
1. Create workflow: run tests, build and push images to Dockerhub (later ECR)
2. Add build statuses

Deliverable: Every push to main builds & pushes new Docker image.

### Milestone 4: Infrastructure as Code (Terraform)

Goal: Provision cloud infra for CI/CD.
1. Use Terraform to create ECR, runners, EKS cluster, DB
2. Create IAM roles to manage and access the env

Deliverable: CI/CD now pushes to AWS ECR instead of DockerHub. 

### Milestone 5: Kubernetes (Local)

Goal: Run your SaaS app in a local k8s cluster.
1. Set up minikube.
2. Write k8s manifests
3. Deployment (backend, frontend).
4. Service (ClusterIP for DB, NodePort/Ingress for frontend/backend).
5. ConfigMaps + Secrets (DB creds).

Deliverable: App accessible at http://localhost:3000.

### Milestone 6: GitOps with ArgoCD

Goal: Automate k8s deployments.

1. Install ArgoCD in your cluster.
2. Create separate GitOps repo with manifests.
3. Configure ArgoCD to sync that repo.

Deliverable: Pushing YAML → Argo updates cluster automatically.

### Milestone 7: Cloud Deployment

Goal: Deploy to cloud k8s.

1. Use Terraform to create an EKS cluster (or DigitalOcean/GKE if simpler).
2. Point ArgoCD at cloud cluster.

Deliverable: The app is live on the internet.

### Milestone 8: Security

Goal: Add security best practices.

1. Add container scanning (Trivy) in CI.
2. Store secrets properly (k8s secrets, or sealed-secrets).
3. Restrict IAM permissions for CI/CD.

Deliverable: Security checks integrated in CI.

### Milestone 9: Observability

Goal: Add monitoring/logging.

1. Install Prometheus + Grafana for metrics.
2. Install Loki/EFK for logs.
3. Add dashboards for app + cluster health.

Deliverable: Grafana dashboard shows your app’s progress data + k8s metrics.
