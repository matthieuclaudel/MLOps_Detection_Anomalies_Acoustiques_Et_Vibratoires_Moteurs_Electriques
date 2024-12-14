Ce répertoire reprend l'orchestration de la solution. En effet, 8 machines doivent accéder à la solution avec un temps de 300ms pour obtenir une prédiction.

Instructions à lancer pour activer Des ports sur la machine hote à partir de docker mini kube.
minikube service multi-port-service-public --url
ou
minikube start --driver=docker --ports 30000:30000 --ports 30001:30001 --ports 30002:30002 --ports 30003:30003 --ports 30004:30004 --ports 8081:8081 --ports 30005:30005 --ports 27017:27017

1. Prometheus
```shell
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install my-kube-prometheus-stack prometheus-community/kube-prometheus-stack --version 66.3.1
Grafana  adminPassword: prom-operator
```
2. Airflow
```shell
helm repo add apache-airflow https://airflow.apache.org/
helm repo update
helm install my-airflow apache-airflow/airflow --version 1.15.0

Airflow Webserver:     kubectl port-forward svc/my-airflow-webserver 8080:8080 --namespace default
Default Webserver (Airflow UI) Login credentials:
    username: admin
    password: admin
Default Postgres connection credentials:
    username: postgres
    password: postgres
    port: 5432
```
3. InfluxDB port 8086
```shell
helm repo add influxdata https://helm.influxdata.com/
helm repo update
helm install my-influxdb2 influxdata/influxdb2 --version 2.1.2
```
InfluxDB 2 is deployed as a StatefulSet on your cluster.

You can access it by using the service name: my-influxdb2

To retrieve the password for the 'admin' user:
```shell
  echo $(kubectl get secret my-influxdb2-auth -o "jsonpath={.data['admin-password']}" --namespace default | base64 --decode)
```
4. MongoDB port 27017
```shell
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add cowboysysop https://cowboysysop.github.io/charts/
helm repo update
helm install my-mongodb bitnami/mongodb --version 16.3.3 -f kubernetes/values-mongodb.yaml
helm install my-mongo-express cowboysysop/mongo-express --version 6.5.2 -f kubernetes/values-mongo-express.yaml
helm upgrade my-mongo-express cowboysysop/mongo-express --version 6.5.2 -f kubernetes/values-mongo-express.yaml
```
NAME: my-mongodb
LAST DEPLOYED: Tue Dec 10 18:04:22 2024
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: mongodb
CHART VERSION: 16.3.3
APP VERSION: 8.0.4

** Please be patient while the chart is being deployed **

MongoDB&reg; can be accessed on the following DNS name(s) and ports from within your cluster:

    my-mongodb.default.svc.cluster.local

To get the root password run:

    export MONGODB_ROOT_PASSWORD=$(kubectl get secret --namespace default my-mongodb -o jsonpath="{.data.mongodb-root-password}" | base64 -d)

To get the password for "adrien" run:

    export MONGODB_PASSWORD=$(kubectl get secret --namespace default my-mongodb -o jsonpath="{.data.mongodb-passwords}" | base64 -d | awk -F',' '{print $1}') 

To get the password for "matthieu" run:

    export MONGODB_PASSWORD=$(kubectl get secret --namespace default my-mongodb -o jsonpath="{.data.mongodb-passwords}" | base64 -d | awk -F',' '{print $2}') 

To get the password for "api" run:

    export MONGODB_PASSWORD=$(kubectl get secret --namespace default my-mongodb -o jsonpath="{.data.mongodb-passwords}" | base64 -d | awk -F',' '{print $3}') 

To get the password for "api_ui" run:

    export MONGODB_PASSWORD=$(kubectl get secret --namespace default my-mongodb -o jsonpath="{.data.mongodb-passwords}" | base64 -d | awk -F',' '{print $4}') 

To connect to your database, create a MongoDB&reg; client container:

    kubectl run --namespace default my-mongodb-client --rm --tty -i --restart='Never' --env="MONGODB_ROOT_PASSWORD=$MONGODB_ROOT_PASSWORD" --image docker.io/bitnami/mongodb:8.0.4-debian-12-r0 --command -- bash

Then, run the following command:
    mongosh admin --host "mongodb" --authenticationDatabase admin -u $MONGODB_ROOT_USER -p $MONGODB_ROOT_PASSWORD

To connect to your database from outside the cluster execute the following commands:

    kubectl port-forward --namespace default svc/mongodb 27017:27017 &
    mongosh --host 127.0.0.1 --authenticationDatabase admin -p $MONGODB_ROOT_PASSWORD

To access the MongoDB&reg; Prometheus metrics, get the MongoDB&reg; Prometheus URL by running:

    kubectl port-forward --namespace default svc/my-mongodb-metrics 9216:9216 &
    echo "Prometheus Metrics URL: http://127.0.0.1:9216/metrics"

Then, open the obtained URL in a browser.

WARNING: There are "resources" sections in the chart not set. Using "resourcesPreset" is not recommended for production. For production installations, please set the following values according to your workload needs:
  - arbiter.resources
  - metrics.resources
  - resources
+info https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/

6. http://inteva.hopto.org:30001/docs               model fastapi
7. http://inteva.hopto.org:30002/Test_prediction    streamlit