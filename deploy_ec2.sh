#!/bin/bash

# project env var is needed in python script
export PROJECT=$1
export AWS_DEFAULT_REGION=us-east-1


echo "########## initializing the project..."
echo ""

mkdir ec2-all-env
cd ec2-all-env

# name needs to be exactly sample-app or app as these are existing templates
cdk init app --language python

python3 -m venv .venv
. .venv/bin/activate

pip install -r requirements.txt

# now overwrite content of app.py with your needed resources
cp ../ec2-all-env.py app.py 

# for ec2 we need configure.sh
echo '#!/bin/sh
# Use this file to install software packages in Amazon Linux

sudo yum -y install iotop' > configure.sh


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


echo "########## to connect to the test vm with ssm run following commands" 
echo 'curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb" -o "session-manager-plugin.deb"
sudo dpkg -i session-manager-plugin.deb
test_ec2_id=$(aws ec2 describe-instances --filters "Name=tag:Name,Values=ec2-instance/vm-${PROJECT}-test" --output text --query 'Reservations[*].Instances[*].InstanceId')
aws --region us-east-1 --profile default ssm start-session --target "$test_ec2_id"
sh-4.2$ sudo iotop'


echo "########## to delete the resources use: cd ec2-all-env; cdk destroy"
