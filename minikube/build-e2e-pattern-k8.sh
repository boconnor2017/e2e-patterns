# Deploys a Minikube container
# Author: Brendan O'Connor
# Date: August 2023

curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && install minikube-linux-amd64 /usr/local/bin/minikube
/usr/local/bin/minikube version
curl -Lo kubectl https://storage.googleapis.com/kubernetes-release/release/v1.23.1/bin/linux/amd64/kubectl && chmod +x kubectl && cp kubectl /usr/local/bin/ && rm kubectl
kubectl version --client
systemctl start docker.service
minikube start --force --driver=docker
