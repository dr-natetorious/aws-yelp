#!/usr/bin/env python3
import os.path
from aws_cdk import (
    aws_s3 as s3,
    aws_iam as iam,
    aws_lambda as lambda_,
    core
)

src_root_dir = os.path.join(os.path.dirname(__file__),"..")

class PhotoResizer(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a layer for function dependencies...
        dependencies_layer = lambda_.LayerVersion(self,'YelpPhotoResizerDeps',
            code=lambda_.Code.from_asset(
                os.path.join(src_root_dir, 'lambda/layers/photo-deps/')),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_8],
            description="Dependencies of lambda://yelp-photo-resize")

        # Create the lambda function itself...
        resizer_lambda = lambda_.Function(self,"yelp-photo-resizer",
            code=lambda_.Code.from_asset(
                os.path.join(src_root_dir, 'lambda/yelp-photo-resize/')),
            runtime= lambda_.Runtime.PYTHON_3_8,
            handler="lambda_function.lambda_handler",
            tracing= lambda_.Tracing.ACTIVE,
            memory_size=256,
            timeout= core.Duration.seconds(60),
            layers=[dependencies_layer])

        # Attach policies neccessary for the code to work
        for policyName in ['AWSXrayWriteOnlyAccess','AmazonS3FullAccess','AmazonDynamoDBFullAccess']:
            resizer_lambda.role.add_managed_policy(
                iam.ManagedPolicy.from_aws_managed_policy_name(policyName))

app = core.App()
PhotoResizer(app, "yelp-photo-resizer")

app.synth()
