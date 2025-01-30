# Diabetes prediction
## Note
+ jenkins_docker folder: deploy jenkins using docker
+ monitoring_docker folder: deploy observable systems using docker
## Table of contents
1. [System Architecture](#1-system-architecture)
2. [Installation](#2-installation)
3. [FastAPI](#3-fastapi)
4. [Observable systems](#4-observable-systems)
    1. [ElasticSearch](#41-elasticsearch)
    2. [Prometheus + Grafana + Jaegar](#42-prometheus--grafana--jaegar)
5. [Jenkins](#5-jenkins)
## 1. System Architecture
## 2. Installation
+ Tested on Python 3.10, recommended to use a virtual environment like Conda
+ Install requirements: ```pip install -r requirements.txt```
+ EDA + Modeling + Training code: [notebooks/diabetes-predict.ipynb](notebooks/diabetes-predict.ipynb)
+ Data: [data/pima-indians-diabetes.csv](data/pima-indians-diabetes.csv)
+ Docker engine
+ Docker images:
    + [khaibk21/predict-diabetes](https://hub.docker.com/repository/docker/khaibk21/predict-diabetes/general): build diabetes prediction service
    + [fullstackdatascience/jenkins:lts](https://hub.docker.com/r/fullstackdatascience/jenkins/tags): build Jenkins service
    + [fullstackdatascience/jenkins-k8s/lts](https://hub.docker.com/r/fullstackdatascience/jenkins-k8s): build Jenkins service + Helm
## 3. FastAPI
+ ```uvicorn main:app --host 0.0.0.0 --port 4001 --reload```
+ ```ngrok http 4001```
+ You can use the address randomly generated from the code above to access the service.
## 4. Observable systems
### 4.1. ElasticSearch
#### How to guide
+ Enter the following codes in the terminal
```bash
cd monitoring-docker/elk
docker compose -f elk-docker-compose.yml -f extensions/filebeat/filebeat-compose.yml up -d
```
+ You can access Kibana at port 5061 to search logs, which FileBeat pulls from containers and pushes to ElasticSearch. Username and password of Kibana can be found at ```monitoring-docker/elk/.env```
### 4.2. Prometheus + Grafana + Jaegar
#### How to guide
+ Start Prometheus, Grafana (to see metrics), and Jaeger Tracing (to see traces) as follows
```bash
cd monitoring-docker
docker compose -f prom-graf-docker-compose.yaml up -d
```
+ Run a container so that `Filebeat` can collect logs from it
```bash
cd instrument
docker build -t foo -f logs/Dockerfile . && docker run -p 8000:8000 --name demo-logs foo
```
+ Run the app to demonstrate metrics
```bash
cd instrument
docker build -t foo-metrics -f metrics/Dockerfile . && docker run -p 8000:8000 --name demo-metrics foo-metrics
```
+ Access services:
    + Prometheus: http://localhost:9090
    + Grafana: http://localhost:3000 with `username/password` is `admin/admin`
    + Kibana: http://localhost:5601 with `username/password` is `elastic/changeme`
    + Jaeger: http://localhost:16686
## 5. Jenkins
#### How to guide
+ ```docker compose -f jenkins_docker/docker-compose.yml up -d```
+ Access service: http://localhost:8081
+ Connect to github repo using ngrok
+ In **Let me select individual events** in **Setting/Webhooks/Manage webhook**, tick **Pull requests** and **Pushes** to inform Jenkins to run whenever we push or pull code from Github.
+ In Jenkins, click **New item** to create new **Multibranch Pipeline**
+ In **Configuration/Branch Sources**, choose **Github** in **Add source**. Then, click **Add**, choose the multibranch pipeline created before to configure the Github account.
+ In **Credentials**, click **global** in **Stores scoped**, then click **Add Credentials** to add Docker Hub account.