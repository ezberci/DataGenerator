repo="europe-west3-docker.pkg.dev/data-generator-363818/data-generator-repo"
------------------------------------------------------------------------
Spark base image build

./spark-3.3.0-bin-hadoop3/bin/docker-image-tool.sh -r $repo -t base -p ./spark-3.3.0-bin-hadoop3/kubernetes/dockerfiles/spark/bindings/python/Dockerfile build

docker push $repo/spark-py:base
------------------------------------------------------------------------
Data generator image build

docker build -f generator-base.Dockerfile  -t pyspark_data_generator:base .

docker tag pyspark_data_generator:base $repo/pyspark_data_generator:base

docker push $repo/pyspark_data_generator:base
------------------------------------------------------------------------
Download key file

gcloud iam service-accounts keys create credentialsFile.json \
--iam-account=data-generator@data-generator-363818.iam.gserviceaccount.com
------------------------------------------------------------------------
kubectl create serviceaccount spark
kubectl create namespace spark
kubectl create clusterrolebinding spark-role --clusterrole=edit --serviceaccount=default:spark --namespace=spark
