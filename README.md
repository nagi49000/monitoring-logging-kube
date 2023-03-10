# monitoring-logging-kube
Play area for doing logging and monitoring in Kubernetes

This repo contains a bunch of services to run in Kubernetes (tested on minikube version: v1.27.1). The helm charts used contain:
- a simple web service with a fluentd (tested on v1.15.3) sidecar
- an elastic instance (tested on 8.5.1) for centralised logging
- a kibana instance (tested on 8.5.1)
- a pod with a prometheus (tested on 2.41.0) and grafana (tested on 9.3.6) instances for centralised monitoring

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


### App and fluentd setup

This is a simple test app that will supply messages for logging and monitoring. The app itself is a simple web server, and has a fluentd sidecar that facilitates monitoring and logging for the app.

The images for the setup are in [services/parrot-api](services/parrot-api/README.md) and [services/fluentd](services/fluentd/README.md). The images can be build directly into minikube's image registry with
```
# in services/parrot-api
minikube image build . -t web
# in services/fluentd
minikube image build . -t fluentd:edge
```

There is a [helm chart](helm/simple-app) (which as a part of the fluentd setup, assumes that elastic has been installed via helm - see the [Elastic section](#elastic-setup)) which can be installed by
```
# in helm
helm install --set ingress.prefixpath=/parrot-api/v1 simple-app ./simple-app/
```

Once up, the service should be available through its ingress
```
curl http://$(minikube ip)/parrot-api/v1/hello_world
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
helm install --set imageTag="8.5.1" --set secret.password=changeme --set replicas=1 elasticsearch elastic/elasticsearch
```

If minikube is unable to pull the requested images directly, then you may have to pull the images manually by connecting to the internal minikube registry, and pulling the images directly into minikube

```
eval $(minikube docker-env)
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.5.1
docker pull docker.elastic.co/kibana/kibana:8.5.1
```

Kibana can be installed with
```
helm install --set imageTag="8.5.1" kibana elastic/kibana
```

The username for logging into elastic is "elastic", and the password (as defined at the elastic install stage) is "changeme", which can also be picked up from
```
kubectl get secrets --namespace=default elasticsearch-master-credentials -ojsonpath='{.data.password}' | base64 -d
```

Using
```
kubectl port-forward service/kibana-kibana 15601:5601
```
the Kibana UI can be accessed [here](http://localhost:15601/).

Similarly, one can check the elastic REST API (which will be using https) using
```
kubectl port-forward service/elasticsearch-master 19200:9200
```
And contacting the service on the host with ```curl -k https://elastic:changeme@localhost:19200/```


### Monitoring and Prometheus setup

Most Prometheus and Grafana helm charts create a number of k8s artefacts (e.g. clusterroles) for hooking into the k8s control plane. There is a [simple helm chart](helm/prometheus-grafana) in this repo for a basic setup.
```
# in helm
helm install prom ./monitoring
```

One can verify that fluent messages are going into prometheus by
```
kubectl port-forward  service/prom-monitoring-prometheus 19090:9090
```
going [here](http://localhost:19090), and executing the PromQL query ```{__name__!=""}```.

and that the Grafana dashboards are live by
```
kubectl port-forward  service/prom-monitoring-grafana 13000:3000
```
and going [here](http://localhost:13000). One can then create dashboards and alerts in Grafana based on the prometheus data source (which will expose the metrics collected from fluentd) as described on the [prometheus grafana docs](https://prometheus.io/docs/visualization/grafana/).

If minikube is unable to pull the requested images directly, then you may have to pull the images manually by connecting to the internal minikube registry, and pulling the images directly into minikube

```
eval $(minikube docker-env)
docker pull prom/prometheus
docker pull grafana/grafana
```
