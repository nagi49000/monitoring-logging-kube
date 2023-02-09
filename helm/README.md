# Deploying a simple app to Kubernetes via helm

Instead of directly using kubernetes manifests, helm can be used. This guide assumes that the app image is built and is in the minikube image registry as per [k8s](../k8s/README.md).

### Out-of-the-box operation

The manifests can be installed by
```
# in fastapi-docker-kube/helm/
helm install app-v1 ./simple-app
```

The installation should appear in the list of installed helm charts
```
helm list
```

The installation can be removed by
```
helm uninstall app-v1
```

### Custom operation

The installation for a particular release can be modified by a custom values file (which can be a modified copy or subset of the [chart values](simple-app/values.yaml) ) by
```
# in fastapi-docker-kube/helm/
helm install -f <custom values yaml> <release name> ./simple-app
```