#!/bin/bash

# project env var is needed in python script
export PROJECT=$1
export AWS_DEFAULT_REGION=us-east-1


echo "########## initializing the project..."
echo ""

mkdir s3-all-env
cd s3-all-env

# name needs to be exactly sample-app or app as these are existing templates
cdk init app --language python

python3 -m venv .venv
. .venv/bin/activate

pip install -r requirements.txt

# now overwrite content of app.py with your needed resources
cp ../s3-all-env.py app.py 

# for s3 we need randomstr module to make s3 name unique
echo "import string
import random

def str_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# to execute use:
# from randomstr import str_generator
# str_generator()" > randomstr.py


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


echo "########## upload demo file to test bucket"

echo "test" > test_s3_bucket_file.txt
mytestbucket=$(aws s3 ls | awk '{print $3}' |grep ${PROJECT}-s3-test)
aws s3 cp test_s3_bucket_file.txt s3://$mytestbucket/
aws s3api list-objects --bucket $mytestbucket --query 'Contents[].Key' --output text


echo "########## to delete the resources use: cd s3-all-env; cdk destroy"
