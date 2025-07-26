# Manual Kubernetes Deployment Guide for Student API

This guide walks through the step-by-step deployment of the full Student API stack in a Minikube-based multi-node Kubernetes cluster. Helm is only used for third-party tools like Vault and External Secrets.

---

## 1. Create Minikube Cluster

```bash
minikube start --nodes=3 -p one2n

kubectl label node one2n type=application
kubectl label node one2n-m02 type=database
kubectl label node one2n-m03 type=dependent_services
```

## 2. Install Helm

Install Helm (if not already installed) using the official docs: https://helm.sh/docs/intro/install/

---

## 3. Deploy Vault and External Secrets via Helm (on dependent_services node)

```bash
helm install vault hashicorp/vault --version 0.30.0 --namespace vault --create-namespace   --set server.dataStorage.storageClass=csi-hostpath-wffc   --set server.securityContext.runAsUser=100   --set server.securityContext.fsGroup=100   --set "server.nodeSelector.type=dependent_services"   --set server.dataStorage.size=100Mi

helm install external-secrets external-secrets/external-secrets --namespace external-secrets   --create-namespace --set installCRDs=true   --set "nodeSelector.type=dependent_services"
```

---

### Note on Storage Class

- The default Minikube storage class `minikube-hostpath` may fail due to security context issues (`fsGroup`).
- Use CSI-compatible driver by enabling the addon:

```bash
minikube addons enable csi-hostpath-driver -p one2n
```

- Create a compatible StorageClass (WaitForFirstConsumer):

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

---

## 4. Vault Initialization & Secret Setup

```bash
kubectl exec -it vault-0 -n vault -- /bin/sh
vault operator init
vault operator unseal <unseal-key-1>
vault operator unseal <unseal-key-2>
vault operator unseal <unseal-key-3>
vault login <root-token>

vault secrets enable -path=secret kv

vault kv put secret/database/creds   DB_USER=<user> POSTGRES_USER=<user>   DB_PASSWORD=<pwd> POSTGRES_PASSWORD=<pwd>

vault token create
```

Use the generated token to create Kubernetes native secret:

```bash
kubectl create secret generic vault-token   --from-literal=token=<token>   -n student-api
```

---

## 5. Deploy Application Manually

```bash
kubectl create ns student-api
```

Apply resources in order:

```bash
kubectl apply -f secretstore-vault.yml
kubectl apply -f external-secret.yml
kubectl apply -f database.yml
kubectl apply -f application.yml
```

ConfigMap for DB host/port/name should be defined in `database.yml` and not hardcoded.

---

## 6. Access the API

```bash
kubectl get svc api -n student-api
minikube ip -p one2n
```

Use the `<NodeIP>:<NodePort>` in your Postman collection to test the API endpoints.

---

That's it. Everything should now be wired up with proper secrets and configs. If anything fails, look at pod logs and service status. Wait for Helm pods to be fully ready before proceeding.