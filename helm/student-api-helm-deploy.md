# Student API - How to Deploy with Helm on Kubernetes

This guide tell you how to use this repo to deploy Student API app on a Kubernetes cluster with Helm. Follow steps to setup infrastructure, Vault, and app stack. All config files already in repo, so you just run commands.

## What You Need

- Minikube installed and running
- Helm installed
- kubectl setup for Minikube context
- Postman to test API
- Repo cloned with helm/values folder ready

## Step 1: Setup Infrastructure

### Start Minikube and Label Nodes

Start Minikube with 3 nodes and label them for app, database, and services:

```bash
minikube start --nodes=3 -p one2n

kubectl label node one2n type=application &&
kubectl label node one2n-m02 type=database &&
kubectl label node one2n-m03 type=dependent_services
```

### Setup StorageClass

Vault need special StorageClass. Run this to create it:

```bash
kubectl apply -f - <<EOF
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: csi-hostpath-wffc
provisioner: hostpath.csi.k8s.io
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Delete
EOF
```

Enable CSI driver addon:

```bash
minikube addons enable csi-hostpath-driver -p one2n
```

## Step 2: Setup Vault (Manual)

### Deploy Vault

Install Vault using Helm chart in repo:

```bash
helm install vault ./charts/vault \
  -f values/vault-values.yaml \
  --namespace vault \
  --create-namespace
```

### Initialize and Unseal Vault

Get into Vault pod and init it:

```bash
kubectl exec -it vault-0 -n vault -- /bin/sh
vault operator init
```

Save unseal keys and root token somewhere safe! Unseal Vault with:

```bash
vault operator unseal <key1>
vault operator unseal <key2>
vault operator unseal <key3>
```

Login and enable secrets:

```bash
vault login <root-token>
vault secrets enable -path=secret kv
```

### Store DB Credentials

Add database credentials to Vault:

```bash
vault kv put secret/database/creds \
  DB_USER=<username> POSTGRES_USER=<username> \
  DB_PASSWORD=<password> POSTGRES_PASSWORD=<password>
```

### Create Vault Token

Create token for external secrets and store in Kubernetes:

```bash
vault token create
kubectl create ns student-api

kubectl create secret generic vault-token \
  --from-literal=token=<vault_token_here> \
  -n student-api
```

## Step 3: Deploy External Secrets Operator

Run this to install External Secrets Operator:

```bash
helm install external-secrets ./charts/external-secrets \
  -f values/external-secrets-values.yaml \
  --namespace external-secrets \
  --create-namespace \
  --wait
```

## Step 4: Deploy App Stack

### Deploy Umbrella Chart

Go to umbrella chart folder and deploy everything:

```bash
cd helm/student-api-stack

# Clean old dependencies
rm -rf charts/ Chart.lock

# Build dependencies
helm dependency build

# Deploy app stack
helm install student-api-stack . --namespace student-api --wait --timeout=15m
```

## Step 5: Test and Verify

### Test API

Get service details to test API in Postman:

```bash
kubectl get svc -n student-api
minikube ip -p one2n
```

Use `<minikube-ip>:<node-port>` as base URL in Postman.

### Check Everything

Verify all components running:

```bash
# Check pods
kubectl get pods -n student-api
kubectl get pods -n vault

# Check secrets
kubectl get secrets -n student-api
kubectl describe externalsecret -n student-api

# Check External Secrets Operator
kubectl get pods -n student-api -l app.kubernetes.io/name=external-secrets
```

## Quick Commands to Deploy

Run these commands in order for full deployment:

```bash
# Infrastructure
minikube start --nodes=3 -p one2n
kubectl label node one2n type=application
kubectl label node one2n-m02 type=database
kubectl label node one2n-m03 type=dependent_services
kubectl apply -f helm/values/storageclass.yaml
minikube addons enable csi-hostpath-driver -p one2n

# Vault
helm install vault ./charts/vault -f values/vault-values.yaml --namespace vault --create-namespace
# ... do vault init, unseal, and config (see Step 2) ...

# External Secrets
helm install external-secrets ./charts/external-secrets -f values/external-secrets-values.yaml --namespace external-secrets --wait

# App Stack
cd helm/student-api-stack
rm -rf charts/ Chart.lock
helm dependency build
helm install student-api-stack . --namespace student-api --wait --timeout=15m
```

## Cleanup

To remove everything:

```bash
helm uninstall student-api-stack -n student-api
helm uninstall external-secrets -n external-secrets
helm uninstall vault -n vault
kubectl delete ns student-api vault
```

## Repo Structure

```
helm/
├── charts/
│   ├── vault/
│   ├── external-secrets/
│   ├── secrets-bridge/
│   ├── postgresql/
│   └── rest-api/
├── student-api-stack/                # Umbrella chart
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── charts/                       # Built by helm dependency build
│   └── templates/
├── values/                           # Config files
└── student-api-helm-deploy.md        # This guide
```

## Troubleshoot Tips

### Vault Issues

- Make sure Vault unsealed before deploying ESO or app stack
- Check Vault token permissions
- Verify secrets stored right in Vault

### External Secrets Issues

- Check ESO pods: `kubectl get pods -n student-api -l app.kubernetes.io/name=external-secrets`
- Verify CRDs: `kubectl get crd | grep external-secrets`
- Ensure ESO connect to Vault

### App Deployment Issues

- Clean dependencies: `rm -rf charts/ Chart.lock` before `helm dependency build`
- Check logs: `kubectl logs -n student-api <pod-name>`
- Verify secrets synced: `kubectl describe externalsecret -n student-api`
- Make sure database up before API deploy

### Resource Conflicts

- If see "exists and cannot be imported" error, clean dependencies and rebuild
- Check Chart.yaml in student-api-stack match setup

## Step 6: Setup ArgoCD and CI/CD Pipeline

### Deploy ArgoCD

Install ArgoCD to manage the application deployment:

```bash
kubectl create namespace argocd
helm install argocd argo/argo-cd -f argocd/argocd-values.yaml --namespace argocd
```

Access the ArgoCD UI:

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Open https://localhost:8080 in a browser. Use username `admin` and get the password:

```bash
kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath='{.data.password}' | base64 -d
```

### Configure ArgoCD Application

Apply the ArgoCD application configuration to monitor the Helm chart:

```bash
kubectl apply -f argocd/argocd-application.yaml
```

### Configure Repository Secret

Apply the repository secret for ArgoCD to access the Git repository:

```bash
kubectl apply -f argocd/argocd-repo-secret.yaml
```

### Source of Truth

The source of truth for the application is the `helm/student-api-stack/values.yaml` file in the Git repository (https://github.com/pmgoriya/SRE-Bootcamp-One2N.git, master branch). ArgoCD monitors this file and automatically syncs changes to the student-api namespace when the `rest-api.image.tag` is updated by the CI pipeline.

## CI/CD Pipeline

The CI pipeline is defined in `.github/workflows/ci.yml`. It:

- Triggers on pushes to master with changes in `students_fastapi/` or manually via `workflow_dispatch`.
- Runs linters, builds a Docker image (`pmgoriya/one2n-sre-bootcamp:<version>`), and pushes it to Docker Hub.
- Uses semantic-release to bump the version in `package.json` based on Conventional Commits (`feat:`, `fix:`).
- Updates `helm/student-api-stack/values.yaml` with the new image tag and commits with `[skip ci]`.
- Requires `contents: write` permissions for `GITHUB_TOKEN`.

To trigger the pipeline manually:

- Go to the GitHub repository (https://github.com/pmgoriya/SRE-Bootcamp-One2N).
- Navigate to the Actions tab, select ci, and click Run workflow.

### Run CI Pipeline Locally

Run the existing `./run.sh` script to simulate the CI pipeline locally:

```bash
./run.sh
```

## Troubleshoot ArgoCD and CI/CD

### ArgoCD Sync Issues:

- Verify repository secret: `kubectl get secret -n argocd -l argocd.argoproj.io/secret-type=repository`
- Check application: `argocd app get student-api-stack -n argocd`
- Force sync: `argocd app sync student-api-stack -n argocd`
- Check logs: `kubectl logs -n argocd -l app.kubernetes.io/name=argocd-application-controller`

### CI Pipeline Issues:

- Check Actions logs in GitHub for semantic-release or Docker errors.
- Verify `package.json` and `values.yaml` updates after runs.
- Ensure Conventional Commits (`feat:`, `fix:`) for version bumps.