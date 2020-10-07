from aws_cdk import (
    aws_s3 as s3,
    core
)


class HelloWorldStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.my_bucket = s3.Bucket(self,"MyFirstBucket", versioned=False)
        self.my_second = s3.Bucket(self, "SecondBucket")
        
