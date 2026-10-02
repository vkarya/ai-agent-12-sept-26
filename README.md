# AI Daily Workflow Agent

This project implements a LangGraph-driven workflow for a daily personal productivity assistant with these responsibilities:

1. Read new emails from an upstream mail service.
2. Check whether any calendar events are scheduled for the current day.
3. Trigger a 9 AM calendar alert.
4. Generate a 10 AM summary of all new emails.

## Selected framework

LangGraph was chosen over CrewAI for this implementation because the tasks are workflow-driven, time-based, and stateful. The system benefits from explicit graph transitions, deterministic agent routing, and easier deployment into a Kubernetes-based orchestration model.

## Architecture

- API layer: FastAPI service exposes HTTP endpoints for workflow execution.
- Orchestration layer: LangGraph graph coordinates task-specific nodes.
- Scheduling layer: APScheduler triggers daily jobs at 9 AM and 10 AM.
- External adapters: placeholder handlers for email and calendar providers.
- Deployment layer: Docker image + Kubernetes manifests for an EKS-ready deployment.

## Local run

From the project root, create and activate a virtual environment, install dependencies, and start the FastAPI app:

PowerShell:

```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Then open:

```text
http://localhost:8000/health
```

If you are using Command Prompt instead of PowerShell, activate the environment with:

```cmd
.venv\Scripts\activate.bat
```

## Mock demo mode

This project ships with mocked email and calendar responses so it can be demonstrated without a live server or credentials.

The app is already configured to run in mock mode by default. After starting the app locally, call the API:

```bash
curl http://localhost:8000/health
```

```bash
curl -X POST http://localhost:8000/tasks/run \
  -H "Content-Type: application/json" \
  -d '{
    "task_name": "calendar_alert",
    "emails": [{
      "subject": "Customer update",
      "from_email": "ops@example.com",
      "snippet": "Please review the proposal"
    }],
    "today_events": [{
      "title": "Daily standup",
      "start": "2026-09-28T09:00:00Z"
    }]
  }'
```

```powershell
curl.exe -X POST http://localhost:8000/tasks/run -H "Content-Type: application/json" -d "{\"task_name\":\"email_brief\",\"emails\":[{\"subject\":\"Quarterly forecast\",\"from\":\"finance@example.com\",\"snippet\":\"Revenue is ahead of target\"}]}"
```

Example output:

```json
{
  "status": "alert_created",
  "alert_message": "Calendar alert: You have today's events scheduled at 9 AM: Daily standup, Client demo. Prioritize these new messages: Follow-up on onboarding, Customer issue update, Security patch reminder.",
  "brief": "Key email brief:\n- Follow-up on onboarding ..."
}
```

The real email/calendar API retrieval code remains in the connector file as commented examples and can be enabled later when credentials are available.

## Docker build and local image

To package the app as a Docker image:

```powershell
docker build -t ai-agent-orchestrator:local .
docker images
```

This builds the image defined in the project Dockerfile and exposes port 8000.

## Kubernetes deployment (Docker Desktop / local cluster)

This project already includes base Kubernetes manifests under `k8s/base` for a simple deployment. For a local Docker Desktop Kubernetes cluster, the easiest flow is to build the image locally and deploy it with `kubectl`.

### 1. Enable Kubernetes in Docker Desktop

1. Open Docker Desktop.
2. Go to Settings > Kubernetes.
3. Enable Kubernetes.
4. Wait for the cluster to become ready.
5. Verify:

```powershell
kubectl version --client
kubectl config current-context
kubectl get nodes
```

You should see a context such as `docker-desktop` and a Ready node.

### 2. Prepare the image for the local cluster

The local deployment uses the Docker image tag already configured in the manifest:

```yaml
image: ai-agent-orchestrator:local
imagePullPolicy: IfNotPresent
```

Build it locally before deploying:

```powershell
docker build -t ai-agent-orchestrator:local .
```

If you are using a private registry or a remote cluster, change the image to your registry tag instead, but for Docker Desktop Kubernetes, the local image tag is the easiest starting point.

### 3. Apply the namespace and app resources

From the project root:

```powershell
kubectl apply -f k8s/base/namespace.yaml
kubectl apply -k k8s/base
```

This creates the namespace and deploys the application, service, and auto-scaling configuration.

### 4. Check workload status

```powershell
kubectl get pods -n ai-productivity
kubectl get svc -n ai-productivity
kubectl get hpa -n ai-productivity
kubectl describe deployment ai-agent-orchestrator -n ai-productivity
```

If the pod is stuck in Pending or CrashLoopBackOff, inspect logs:

```powershell
kubectl logs -n ai-productivity deploy/ai-agent-orchestrator
```

### 5. Test the deployed app

Port-forward the service to your local machine:

```powershell
kubectl port-forward -n ai-productivity svc/ai-agent-orchestrator 8000:80
```

Then test the health endpoint:

```bash
curl http://localhost:8000/health
```

```summary
docker build -t ai-agent-orchestrator:local .
kubectl apply -f k8s/base/namespace.yaml
kubectl apply -k k8s/base
kubectl get pods -n ai-productivity
kubectl get svc -n ai-productivity
kubectl port-forward -n ai-productivity svc/ai-agent-orchestrator 8000:80
````

And trigger the workflow:

```bash
curl -X POST http://localhost:8000/tasks/run \
  -H "Content-Type: application/json" \
  -d '{
    "task_name": "calendar_alert",
    "emails": [{
      "subject": "Customer update",
      "from_email": "ops@example.com",
      "snippet": "Please review the proposal"
    }],
    "today_events": [{
      "title": "Daily standup",
      "start": "2026-09-28T09:00:00Z"
    }]
  }'
```

### 6. Kubernetes cleanup

```powershell
kubectl delete -k k8s/base
kubectl delete namespace ai-productivity
```

## Production deployment notes

The repository includes Kubernetes manifests under `k8s/base` for a simple EKS-ready deployment. For production, move the image to a real registry such as Amazon ECR, update the image value in the deployment, and set secure environment variables via Kubernetes secrets or a secret manager.

## Notes

- Replace the mock email/calendar connectors with real integrations such as Microsoft Graph or Gmail/Google Calendar.
- Use a managed secret store such as AWS Secrets Manager or External Secrets for API keys.
- Add monitoring with Prometheus/Grafana and logs through CloudWatch or Fluent Bit.
- The app reads environment variables like `APP_ENV`, `APP_PORT`, `OLLAMA_BASE_URL`, `OLLAMA_MODEL`, `LOG_LEVEL`, and `SCHEDULER_TIMEZONE`; for Kubernetes, these can be supplied via `env:` entries or a mounted secret.

## Notes

- Replace the mock email/calendar connectors with real integrations such as Microsoft Graph or Gmail/Google Calendar.
- Use a managed secret store such as AWS Secrets Manager or External Secrets for API keys.
- Add monitoring with Prometheus/Grafana and logs through CloudWatch or Fluent Bit.
