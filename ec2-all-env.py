import os.path

from aws_cdk.aws_s3_assets import Asset

from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    App, Stack
)

from constructs import Construct

# additional imports
import os
import sys

try:  
   os.environ["PROJECT"]
except KeyError: 
   print ("Please set the environment variable PROJECT")
   sys.exit(1)

project = os.environ["PROJECT"]
print("PROJECT: " + os.environ["PROJECT"])


dirname = os.path.dirname(__file__)


class EC2InstanceStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # AMI
        amzn_linux = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
            )

        # Instance Role and SSM Managed Policy
        role = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))

        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))

        # Create an ec2 vm for every stage
        stages = ["test", "dev", "prod"]
        for stage in stages:
            print("########## Processing infrastructure for the following stage: " + stage + " ...")  

            # VPC
            vpc = ec2.Vpc(self, 'vpc-{}-{}'.format(project, stage),
                nat_gateways=0,
                subnet_configuration=[ec2.SubnetConfiguration(name="public" + "-" + project + "-" + stage,subnet_type=ec2.SubnetType.PUBLIC)]
                )

            # 'vm-{}-{}'.format(project, stage) defines ec2 vm name
            #instance = ec2.Instance(self, 'Instance{}'.format(stage),
            instance = ec2.Instance(self, 'vm-{}-{}'.format(project, stage),
                instance_type=ec2.InstanceType("t3.nano"),
                machine_image=amzn_linux,
                vpc = vpc,
                role = role
                )

            # Script in S3 as Asset
            asset = Asset(self, 'Asset{}'.format(stage), path=os.path.join(dirname, "configure.sh"))
            local_path = instance.user_data.add_s3_download_command(
                bucket=asset.bucket,
                bucket_key=asset.s3_object_key
            )

            # Userdata executes script from S3
            instance.user_data.add_execute_file_command(
                file_path=local_path
                )
            asset.grant_read(instance.role)

app = App()
EC2InstanceStack(app, "ec2-instance")

app.synth()