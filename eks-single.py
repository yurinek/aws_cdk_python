# only single eks because multiple eks per stack not supported

from aws_cdk.lambda_layer_kubectl_v29 import KubectlV29Layer

from aws_cdk import (
    aws_eks as eks,
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


class EKSStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # provisioning a cluster
        cluster = eks.Cluster(self, "test-eks",
            version=eks.KubernetesVersion.V1_29,
            kubectl_layer=KubectlV29Layer(self, "kubectl")
        )

        # apply a kubernetes manifest to the cluster
        cluster.add_manifest("test", {
            "ApiVersion": "v1",
            "kind": "Pod",
            "metadata": {"name": "test"},
            "spec": {
                "containers": [{
                    "name": "hello",
                    "image": "paulbouwer/hello-kubernetes:1.5",
                    "ports": [{"container_port": 8080}]                    
                }
                ]
            }
        })



app = App()
EKSStack(app, "eks-k8s")

app.synth()
