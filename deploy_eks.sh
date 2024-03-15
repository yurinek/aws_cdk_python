#!/bin/bash

# project env var is needed in python script
export PROJECT=$1
export AWS_DEFAULT_REGION=us-east-1


echo "########## initializing the project..."
echo ""

# only single eks k8s cluster is supported per stack
mkdir eks-single
cd eks-single

# name needs to be exactly sample-app or app as these are existing templates
cdk init app --language python

python3 -m venv .venv
. .venv/bin/activate

pip install -r requirements.txt

# now overwrite content of app.py with your needed resources
cp ../eks-single.py app.py 

# for eks we need additional package for k8s version 1.29
pip install aws-cdk.lambda-layer-kubectl-v29


echo "########## cdk ls"
echo ""

# verify the stack works
cdk ls


echo "########## cdk bootstrap"
echo ""

# bootstrap with your AWS account number
cdk bootstrap --trust="$2" --cloudformation-execution-policies=arn:aws:iam::aws:policy/AdministratorAccess


echo "########## cdk synth"
echo ""

# following creates a cloud formation template in cdk.out directory
cdk synth


echo "########## cdk diff"
echo ""

cdk diff


echo "########## cdk deploy"
echo ""

cdk deploy --asset-parallelism=false --require-approval never


echo "########## to create kubeconfig for test k8s cluster connection run following commands" 
echo 'test_k8s=$(aws eks list-clusters --region us-east-1 | jq -r -c '"'"'.clusters[] | select(. | startswith("test"))'"'"')'
# create or update kubeconfig
echo 'aws eks update-kubeconfig --region us-east-1 --name "$test_k8s" --kubeconfig ~/test_kube_aws --profile default'
echo 'export KUBECONFIG=$KUBECONFIG:~/test_kube_aws
kubectl get po test'


echo "########## to delete the resources use: cd eks-single; cdk destroy"
