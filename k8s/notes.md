## Deployment steps

- Create minikube cluster with 3 nodes and label them as per the milestone
- Install helm
- deploy vault and eso on the node mentioned with their respective ns using node affinity, using helm
`helm install vault hashicorp/vault --version 0.30.0 --namespace vault --create-namespace --set server.dataStorage.storageClass=csi-hostpath-sc --set server.securityContext.runAsUser=100 --set server.securityContext.fsGroup=100 --set "server.nodeSelector.type=dependent_services" --set server.dataStorage.size=100Mi`

`helm install external-secrets external-secrets/external-secrets   --namespace external-secrets   --create-namespace   --set installCRDs=true   --set "nodeSelector.type=dependent_services"`

* Note
* In Minikube, the default `minikube-hostpath` storage class doesn't support proper permission handling (`fsGroup`, etc.).
* This causes Vault to fail writing to `/vault/data`, even with root or init containers.
* `csi-hostpath-sc` is a CSI-compliant storage class that supports Kubernetes security contexts.
* Enable it using: `minikube addons enable csi-hostpath-driver -p <profile-name>`.
* Use it with Helm via: `--set server.dataStorage.storageClass=csi-hostpath-sc`.
* Also the default csi sc's config for WaitForFirstConsumer cannot be changed: solves the error: vault cant start until pvc is bound and pod cant be scheduled until pvc is bound.
To solve this problem we need to provision another storage class using the command

`kubectl apply -f - <<EOF
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: csi-hostpath-wffc
provisioner: hostpath.csi.k8s.io
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Delete
EOF`


- Using the port forward command expose the vault service and through its UI create the necessary secrets. (DB_USER, DB_PASSWORD, POSTGRES_PASSWORD)
`kubectl port-forward svc/vault -n vault 8200:8200`

- Create ConfigMap for non-sensitive values (DB_HOST, DB_PORT,DB_NAME)
- Create a secret store which tells the eso which backend to pick up the secrets from.
- Create external secret to map to exact resource