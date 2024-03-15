from aws_cdk import (
    aws_s3 as s3,
    core
)

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


class S3Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create an S3 bucket
        bucket = s3.Bucket(self, "MyBucket",
            bucket_name=project + "-s3-" + str_generated, # specify a unique bucket name
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED
        )

app = core.App()
S3Stack(app, "S3Stack")
app.synth()