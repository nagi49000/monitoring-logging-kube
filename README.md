# monitoring-logging-kube
Play area for doing logging and monitoring in Kubernetes

### Minikube setup

One can use minikube as a test k8s environment for deployment.

The [minikube](https://minikube.sigs.k8s.io/docs/start/) install instructions are a little sparse. [This guide](https://www.linuxtechi.com/how-to-install-minikube-on-ubuntu/) covers more details.

Ingress controllers and additional memory for Elastic etc will be useful, which will need minikube being run with some additional flags

```
minikube start --driver=docker --addons=ingress --install-addons=true --cpus=2 --memory=16g
```

``` minikube delete ``` will clear down the minikube environment, and ``` minikube delete --purge``` will remove all minikube profiles.