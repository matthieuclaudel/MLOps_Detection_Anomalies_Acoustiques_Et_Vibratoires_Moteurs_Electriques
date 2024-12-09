Ce répertoire reprend l'orchestration de la solution. En effet, 8 machines doivent accéder à la solution avec un temps de 300ms pour obtenir une prédiction.

Instructions à lancer pour activer Des ports sur la machine hote à partir de docker mini kube.
minikube service multi-port-service-public --url
ou
minikube start --driver=docker --ports 30000:30000 --ports 30001:30001 --ports 30002:30002 --ports 30003:30003 --ports 30004:30004 --ports 30005:30005

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
