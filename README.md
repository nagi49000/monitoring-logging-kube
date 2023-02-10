# monitoring-logging-kube
Play area for doing logging and monitoring in Kubernetes

### Minikube setup

One can use minikube as a test k8s environment for deployment.

The [minikube](https://minikube.sigs.k8s.io/docs/start/) install instructions are a little sparse. [This guide](https://www.linuxtechi.com/how-to-install-minikube-on-ubuntu/) covers more details.

Ingress controllers and additional memory for Elastic etc will be useful, which will need minikube being run with some additional flags

```
minikube start --driver=docker --addons=ingress --install-addons=true --cpus=5 --memory=16g
```

The k8s instance can be stopped and started with ```minikube stop``` and ```minikube start``` respectively.

```minikube delete``` will clear down the minikube environment, and ```minikube delete --purge``` will remove all minikube profiles.

As a quick way round of building the image locally, and pushing to minikube's container registry (which is what one would normally do with a kubernetes cluster), one can build the image directly in minikube's image registry.

```
# in services/
minikube image build . -t web
minikube image ls
```

### Elastic setup

With minikube running, one can install [elastic via helm](https://github.com/elastic/helm-charts/tree/main/elasticsearch). The repo has full instructions in the readmes. To summarize, the helm repo must be added

```
helm repo add elastic https://helm.elastic.co
helm repo list
```

For minikube, a couple of add ons are needed

```
minikube addons enable default-storageclass
minikube addons enable storage-provisioner
```

A single pod deployment can then be created with

```
helm install --set replicas=1 elasticsearch elastic/elasticsearch
```

If minikube is unable to pull the requested images directly, then you may have to pull the images manually by connecting to the internal minikube registry, and pulling the images directly into minikube

```
eval $(minikube docker-env)
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.5.1
docker pull docker.elastic.co/kibana/kibana:8.5.1
```

Kibana can be installed with
```
helm install kibana elastic/kibana
```

The username for logging into elastic is ```elastic```, and the password can be obtained by
```
kubectl get secrets --namespace=default elasticsearch-master-credentials -ojsonpath='{.data.password}' | base64 -d
```

Using
```
kubectl port-forward service/kibana-kibana 15601:5601
```
the Kibana UI can be accessed [here](http://localhost:15601/).