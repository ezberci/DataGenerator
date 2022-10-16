
# Generating mock data for BigQuery on Google Kubernetes Engine (GKE) using Apache-Spark

## Download necessary files

`wget -c https://dlcdn.apache.org/spark/spark-3.3.0/spark-3.3.0-bin-hadoop3.tgz -O - | tar -xz`

`wget -c wget -c https://github.com/databrickslabs/dbldatagen/releases/download/release%2Fv0.2.1/dbldatagen-0.2.1-py3-none-any.whl`

`wget -c https://storage.googleapis.com/spark-lib/bigquery/spark-3.1-bigquery-0.26.0-preview.jar`

## Set your repository

repo="your-repo"

## Spark base image build

`./spark-3.3.0-bin-hadoop3/bin/docker-image-tool.sh -r $repo -t base -p ./spark-3.3.0-bin-hadoop3/kubernetes/dockerfiles/spark/bindings/python/Dockerfile build`

`docker push $repo/spark-py:base`

## Data generator image build

`docker build -f generator-base.Dockerfile  -t pyspark_data_generator:base .`

`docker tag pyspark_data_generator:base $repo/pyspark_data_generator:base`

`docker push $repo/pyspark_data_generator:base`

## Download key file

`gcloud iam service-accounts keys create credentialsFile.json \
--iam-account=$SERVICE_ACCOUNT_EMAIL`

## Creating kubernetes service account, namespace and permissions.

`kubectl create serviceaccount spark`

`kubectl create namespace spark`

`kubectl create clusterrolebinding spark-role --clusterrole=edit --serviceaccount=default:spark --namespace=spark`

## Spark-submit

You can get your kubernetes cluster ip using “kubectl cluster-info”

`repo="your-repository"`

`kubernetes_cluster_ip="xx.xxx.xxx.xx"`

`./spark-3.3.0-bin-hadoop3/bin/spark-submit \
--master k8s://https://$kubernetes_cluster_ip \
--deploy-mode cluster \
--name data-generator \
--conf spark.executor.instances=1 \
--conf spark.kubernetes.container.image=$repo/data_generator:v1 \
--conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
--jars local:///spark-3.1-bigquery-0.26.0-preview.jar \
--py-files local:///dbldatagen-0.2.1-py3-none-any.whl \
local:///data-generator.py`

