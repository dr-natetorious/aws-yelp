#!/usr/bin/env python3
import os.path
from aws_cdk import (
    aws_s3 as s3,
    aws_lambda as lambda_,
    core
)

src_root_dir = os.path.join(os.path.dirname(__file__),"..")

class PhotoResizer(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.dep_layers = lambda_.LayerVersion(self,'YelpPhotoResizerDeps',
            code=lambda_.Code.from_asset(
                os.path.join(src_root_dir, 'lambda/layer/photo-deps/')),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_8],
            description="Dependencies of lambda://yelp-photo-resize")

        lambda_.Function(self,"yelp-photo-resizer",
            code=lambda_.Code.from_asset(
                os.path.join(src_root_dir, 'lambda/yelp-photo-resize/')),
            runtime= lambda_.Runtime.PYTHON_3_8,
            handler="lambda_function.lambda_handler",
            layers=[self.dep_layers])

app = core.App()
PhotoResizer(app, "yelp-photo-resizer")

app.synth()
