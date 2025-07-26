# Student API - End-to-End Kubernetes Helm Deployment Guide

This document outlines the step-by-step Helm-based deployment process for the Student API app, following the strict chart structure and configuration separation.

---

## Prerequisites

- Minikube installed and running
- Helm installed
- `kubectl` configured with Minikube context
- Postman (for API testing)
- All `values.yaml` files prepared inside the `helm/values` directory

---

## 1. Start Minikube and Label Nodes

```bash
minikube start --nodes=3 -p one2n

kubectl label node one2n type=application
kubectl label node one2n-m02 type=database
kubectl label node one2n-m03 type=dependent_services
```

---

## 2. Set Up a Compatible StorageClass

Vault requires a storage class that supports `fsGroup`. Default `minikube-hostpath` won’t work.

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

Also make sure this addon is enabled:

```bash
minikube addons enable csi-hostpath-driver -p one2n
```

---

## 3. Deploy Vault

```bash
helm install vault ./charts/vault \
  -f values/vault-values.yaml \
  --namespace vault \
  --create-namespace
```

---

## 4. Deploy External Secrets Operator (ESO)

```bash
helm install external-secrets ./charts/external-secrets \
  -f values/external-secrets-values.yaml \
  --namespace external-secrets \
  --create-namespace
```

---

## 5. Initialize and Unseal Vault

```bash
kubectl exec -it vault-0 -n vault -- /bin/sh
vault operator init
vault operator unseal <key1>
vault operator unseal <key2>
vault operator unseal <key3>

vault login <root-token>
vault secrets enable -path=secret kv
```

Now store the credentials:

```bash
vault kv put secret/database/creds \
  DB_USER=<username> POSTGRES_USER=<username> \
  DB_PASSWORD=<password> POSTGRES_PASSWORD=<password>
```

Then generate a Vault token and store it in Kubernetes:

```bash
vault token create
kubectl create ns student-api

kubectl create secret generic vault-token \
  --from-literal=token=<vault_token_here> \
  -n student-api
```

---

## 6. Deploy Secrets Bridge (SecretStore + ExternalSecret)

```bash
helm install secrets-bridge ./charts/secrets-bridge \
  -f values/secrets-bridge-values.yaml \
  --namespace student-api
```

---

## 7. Deploy PostgreSQL (Uses Secret Ref)

```bash
helm install postgres ./charts/postgresql \
  -f values/postgresql-values.yaml \
  --namespace student-api
```

Wait for DB pods to be fully up and healthy before moving forward.

---

## 8. Deploy FastAPI REST Application

```bash
helm install rest-api ./charts/rest-api \
  -f values/rest-api-values.yaml \
  --namespace student-api
```

---

## 9. Test the API with Postman

Get the IP and NodePort:

```bash
kubectl get svc -n student-api
minikube ip -p one2n
```

Use `<minikube-ip>:<node-port>` as the base URL in your Postman collection.

Make sure all endpoints behave as expected.

---

## 10. Cleanup (Optional)

```bash
helm uninstall rest-api -n student-api
helm uninstall postgres -n student-api
helm uninstall secrets-bridge -n student-api

helm uninstall external-secrets -n external-secrets
helm uninstall vault -n vault

kubectl delete ns student-api vault external-secrets
```

---

## Helm Repository Structure

```
helm/
├── charts/
│   ├── vault/
│   ├── external-secrets/
│   ├── secrets-bridge/
│   ├── postgresql/
│   └── rest-api/
└── values/
    ├── vault-values.yaml
    ├── external-secrets-values.yaml
    ├── secrets-bridge-values.yaml
    ├── postgresql-values.yaml
    └── rest-api-values.yaml
```

Each component is deployed using its own values file. No Helm CLI flags are used to pass values dynamically. All configuration changes should be made in the corresponding `values/*.yaml` files.

---

## Final Notes

- Order matters. Make sure to follow the exact sequence.
- Wait for each deployment to stabilize before jumping to the next.
- If something doesn’t work, check pod logs, secrets, and node selectors.
- Postman testing should work directly once all components are ready.