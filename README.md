# Yelp Dataset on AWS

Scripts and tooling for playing with the [Yelp dataset](yelp.com/dataset/) on AWS.

## Setting up resources

This repository uses the [AWS Cloud Deployment Key](https://docs.aws.amazon.com/cdk/) to provision resources.

A [Dockerfile](cdk/Dockerfile) exists for hosting the CDK and is accessible using the following script

```bash
# These values are specific to your environment
$repo_root=/git/aws-yelp
$image_name=cdk-deploy
$account_id=YOUR_AWS_ACCOUNTID
$region=YOUR_REGION_eg_us-east-2
$deploy_stacks=*

# Build the container...
docker build -t $image_name $repo_root/cdk

# Launch the development environment
$mount_git=-v $repo_root:/aws-yelp
$mount_aws_creds=-v ~/.aws:/root/.aws
$working_dir=-w /aws-yelp/cdk
docker run -it $mount_git $mount_aws_creds $working_dir $image_name bash

# Install any custom python modules
pip install -r requirements.txt

# Bootstrap your account
cdk bootstrap aws://$accountid/$region

# Optionally view the output or changes
cdk synth $deploy_stacks
cdk diff $deploy_stacks

# Deploy repository
cdk deploy $deploy_stacks
```
