# aws_cdk_python

This project deploys AWS infrastructure resources using AWS CDK + Python

## Prerequisits

- Linux OS
- Python 3.0+
- pip3
- AWS account
- access key for AWS user
- make sure to use default profile in ~/.aws

```
cat ~/.aws/credentials 
[default]
aws_access_key_id = XXX
aws_secret_access_key = XXX

cat ~/.aws/config 
[default]
region = us-east-1
```


## Install tools

```
./install.sh
```


## Deploy s3 bucket to 3 stages (test, dev, prod)

```
./deploy_s3.sh myapp aws_account_number
```


## Deploy ec2 vm to 3 stages (test, dev, prod)

```
./deploy_ec2.sh myapp aws_account_number
```


## Deploy eks k8s cluster to test stage (only 1 cluster per stack is supported)

```
./deploy_eks.sh myapp aws_account_number
```


## Comparison to plain Terraform

### CDK advantages

-   any Python code from different software stacks can be reused to build resources with custom logic
-   its possible to add variables into resource names (not possible in Terraform)

### CDK disadvantages

-   cdk works with CloudFormation templates. CloudFormation doesn't directly support creation of EC2 ssh Key Pairs. With custom CF template:
    its not possible to copy only public ssh key to target vm. instead both keys are needed. The private key is stored in AWS Secrets Manager.
-   vendor lock. as copying only ssh public keys to target ec2 vm is not supported, one is forced to use ssm (Amazon alternative to ssh) instead. 
-   vendor lock and security issue. to be able to use ssh keys one is forced to share own ssh private key to AWS Secrets Manager.
-   not possible to dynamically set hostname of ec2 vm
-   subnet names get predifined suffixes which cant be customized
-   only 1 k8s cluster per stack is supported
-   creation of a standard EKS cluster is very slow  
-   EKS cluster deployment often times out
-   there are too many bugs to consider CDK for EKS to be stable
-   works only with AWS cloud


## Tested with

Python 3.8.10  
cdk 2.130.0
