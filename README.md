region: [us-east1]
    zone: [us-east1-d]

docker image id: 
gcr.io/p-g-us-adv-x-dat-aia-proto-1/nathanhuang/kubernetes-jenkins-ci-cd-demo:v1


##############################
# Global parameters
##############################
# project info
GCP_PROJECT_ID=p-g-us-adv-x-dat-aia-proto-1
COMPUTE_ZONE=us-east1-d


# docker image info
CLOUD_IMAGE_NAME=nathanhuang/kubernetes-jenkins-ci-cd-demo
IMAGE_VERSION=v1
CLOUD_IMAGE_DIR=gcr.io/$GCP_PROJECT_ID/$CLOUD_IMAGE_NAME:$IMAGE_VERSION

# kubernete cluster info
CLUSTER_NAME=ml-cluster-dev
CLUSTER_VERSION=1.9.6-gke.0
CLUSTER_NODE_SIZE=3
CLUSTER_MIN_NODES=1
CLUSTER_MAX_NODES=4

##############################
# Troubleshooting matplotlib in MacOSX:
# import matplotlib.pyplot as plt
# [NSApplication _setup:]: unrecognized selector sent to instance 0x7f8a38b72880
##############################
cd ~/.matplotlib
vim matplotlibrc
Input :  `backend : TkAgg`

##############################
# Build Docker Image
##############################
cd Dockerfiles
docker build -t $CLOUD_IMAGE_NAME .


##############################
# Setup gcloud
##############################
gcloud init
gcloud config set project $GCP_PROJECT_ID
gcloud config set compute/zone $COMPUTE_ZONE
gcloud config set container/cluster $CLUSTER_NAME


##############################
# Create Kubernete cluster
##############################
# Create cluster
gcloud container clusters create $CLUSTER_NAME --zone $COMPUTE_ZONE --num-nodes=$CLUSTER_NODE_SIZE --enable-autoscaling --max-nodes=$CLUSTER_MAX_NODES --min-nodes=$CLUSTER_MIN_NODES

# Get cluster credentials locally
gcloud container clusters get-credentials $CLUSTER_NAME


##############################
# Push Docker to Cloud
##############################
docker tag $CLOUD_IMAGE_NAME $CLOUD_IMAGE_DIR
gcloud docker -- push $CLOUD_IMAGE_DIR


##############################
# Troubleshooting  gcloud docker -- push
WARNING! Using --password via the CLI is insecure. Use --password-stdin.
Error response from daemon: Get https://b.gcr.io/v2/: unknown: b.gcr.io domain is disabled. See https://cloud.google.com/container-registry/docs/support/deprecation-notices
ERROR: (gcloud.docker) Docker login failed.
##############################
Disable storing docker credentials on mac os x keychain by removing this entry from your ~/.docker/config.json file.
"credsStore": "osxkeychain",
##############################


##############################
# Create YAML Files
##############################
# create pod yaml file

# create deployment yaml file

# create service yaml file

##############################
# Deploy Image to Kubernetes
##############################
cd ..
kubectl create -f service_n_deployment.yaml


##############################
# Check Status
##############################
kubectl get pods
Kubectl describe pod <pod-id>

kubectl get pods -o wide  



##############################
# 1. Check deployment 
# 2. Expose service
# 3. Get EXTERNAL-IP
##############################
1. kubectl get deployment
2. kubectl expose deployment fake-news-detection-deployment --type=LoadBalancer --port 80 --target-port 80
3. kubectl get service (EXTERNAL-IP)


##############################
#  Delete service
##############################
kubectl get service
kubectl delete services ner-spacy-app-deployment


##############################
#  Delete deployment
##############################
kubectl delete deployment hello-world


##############################
#  Docker run in terminal UTF-8 with large memory
##############################
docker run -it --rm -m 8000M --memory-swap=2000M --entrypoint=/bin/bash gcr.io/p-g-us-adv-x-dat-aia-proto-1/nathanhuang/ner-spacy-deals:v6


##############################
#  Troubleshooting1
#  Issue:
#  Builtins.UnicodeDecodeError
#  UnicodeDecodeError: 'ascii' codec can't decode byte 0xf6 in position 11: ordinal not in range(128)
##############################
`with open('vocab.pkl', 'rb') as fp:
      vocab = pickle.load(fp)`
 Change to:
 `with open('vocab.pkl', 'rb') as fp:
        u = pickle._Unpickler(fp)
        u.encoding = 'latin1'
        vocab = u.load()`

##############################
#  Troubleshooting2
#  Issue:
#  OSError: Failed to interpret file 'idf.p' as a pickle
##############################
1.np.save('idf.npy', idf)
2.idfs = np.load("idf.npy")
`*.p` in linux throws OSError ,change it to `*.npy`





