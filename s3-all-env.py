
from constructs import Construct
from aws_cdk import App, Stack   
from aws_cdk import aws_s3 as s3  
from aws_cdk import RemovalPolicy


# additional imports
from randomstr import str_generator
import os
import sys

try:  
   os.environ["PROJECT"]
except KeyError: 
   print ("Please set the environment variable PROJECT")
   sys.exit(1)

project = os.environ["PROJECT"]
print("PROJECT: " + os.environ["PROJECT"])
# store random string, so all the resources for this run have the same random string in their name
str_generated = str_generator()
print("str_generated: " + str_generated)


class S3Stack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create an S3 bucket for every stage
        stages = ["test", "dev", "prod"]
        for stage in stages:
            print("########## Processing infrastructure for the following stage: " + stage + " ...")  
            bucket = s3.Bucket(self, 'MyBucket{}'.format(stage),
                bucket_name=project + "-s3-" + stage + "-" + str_generated, # specify a unique bucket name
                versioned=True,
                encryption=s3.BucketEncryption.S3_MANAGED,
                removal_policy=RemovalPolicy.DESTROY, # delete this parameter if bucket should not be deleted while stack is destroyed
                auto_delete_objects=True # needed for RemovalPolicy.DESTROY to be successfull for not empty buckets
            )

app = App()
S3Stack(app, "S3Stack")
app.synth()