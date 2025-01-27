# Diabetes prediction
## Note
+ jenkins_docker folder: deploy jenkins using docker
+ monitoring_docker folder: deploy observable systems using docker
+ monitoring_k8s folder: deploy observable systems using k8s
    + monitoring: install necessary objects to deploy Prometheus + Grafana services
    + service_monitor: set up object to scape custom metrics from diabetes service
+ service_k8s folder: deploy service using k8s
    + diabetes_prediction_chart folder: using istio ingress gateway + virtual service to access to diabetes service in the cluster
    + nginx-ingress folder: using to istall nginx
    + service_ingress folder: using nginx ingress to access to diabetes service in the cluster
    + service_wo_ingress foler: using loadbalancer to access to diabetes service in the cluster
## Table of contents
1. [System Architecture](#1-system-architecture)
2. [Installation](#2-installation)
3. [FastAPI](#3-fastapi)
4. [Observable systems](#4-observable-systems)
    1. [ElasticSearch](#41-elasticsearch)
    2. [Prometheus + Grafana + Jaegar](#42-prometheus--grafana--jaegar)
5. [Jenkins](#5-jenkins)
6. [Google Kubernetes Engine](#6-google-kubernetes-engine)
    1. [GKE + Jenkins](#61-gke--jenkins)
    2. [GKE + deploy app and monitoring services](#62-gke--deploy-app-and-monitoring-services)
## 1. System Architecture
## 2. Installation
+ Tested on Python 3.10, recommended to use a virtual environment like Conda
+ Install requirements: ```pip install -r requirements.txt```
+ EDA + Modeling + Training code: [notebooks/diabetes-predict.ipynb](notebooks/diabetes-predict.ipynb)
+ Data: [data/pima-indians-diabetes.csv](data/pima-indians-diabetes.csv)
+ Docker engine
+ Docker images:
    + [fullstackdatascience/jenkins:lts](https://hub.docker.com/r/fullstackdatascience/jenkins/tags): build Jenkins service
    + [fullstackdatascience/jenkins-k8s/lts](https://hub.docker.com/r/fullstackdatascience/jenkins-k8s): build Jenkins service + Helm
## 3. FastAPI

## 4. Observable systems
### 4.1. ElasticSearch

### 4.2. Prometheus + Grafana + Jaegar

## 5. Jenkins

## 6. Google Kubernetes Engine
### 6.1 GKE + Jenkins

### 6.2 GKE + deploy app and monitoring services

