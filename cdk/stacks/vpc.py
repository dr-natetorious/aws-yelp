#!/usr/bin/env python3
from aws_cdk import (
    aws_ec2 as ec2,
    aws_lambda as lambda_,
    core
)

class YelpNetwork(core.Stack):
    """
    Configure and deploy the network
    """
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create the DataNet network
        # CIDR Mask Sizes: https://docs.netgate.com/pfsense/en/latest/network/cidr.html

        self.__dataNet = ec2.Vpc(self, "DataNet", cidr="10.10.0.0/16",
            subnet_configuration= [
                ec2.SubnetConfiguration(
                    name='Postgres-', subnet_type= ec2.SubnetType.ISOLATED, cidr_mask=25)
            ])

        self.__website = ec2.Vpc(self, "Website", cidr="10.20.0.0/16",
            subnet_configuration= [
                    ec2.SubnetConfiguration(
                        name='Public-', subnet_type= ec2.SubnetType.PUBLIC,cidr_mask=24),
                    ec2.SubnetConfiguration(
                        name='MiddleTier-', subnet_type= ec2.SubnetType.ISOLATED,cidr_mask=24)
            ])

        ec2.CfnVPCPeeringConnection(self, "Website-to-DataNet",
            vpc_id=self.__website.vpc_id,
            peer_vpc_id= self.__dataNet.vpc_id)

        self.__corpNet = ec2.Vpc(self, "CorpNet", cidr="10.30.0.0/16",
            subnet_configuration= [
                    ec2.SubnetConfiguration(
                        name='Gateway-', subnet_type= ec2.SubnetType.PUBLIC, cidr_mask=24),
                    ec2.SubnetConfiguration(
                        name='Private-IT-', subnet_type= ec2.SubnetType.ISOLATED, cidr_mask=20),
                    ec2.SubnetConfiguration(
                        name='Private-Finance-', subnet_type= ec2.SubnetType.ISOLATED, cidr_mask=24),
                    ec2.SubnetConfiguration(
                        name='Private-Marketing-', subnet_type= ec2.SubnetType.ISOLATED, cidr_mask=24),
            ])


        ec2.CfnVPCPeeringConnection(self, "CorpNet-to-Website",
            vpc_id=self.__corpNet.vpc_id,
            peer_vpc_id= self.__website.vpc_id)

        ec2.CfnVPCPeeringConnection(self, "CorpNet-to-DataLake",
            vpc_id=self.__corpNet.vpc_id,
            peer_vpc_id= self.__dataNet.vpc_id)

    @property
    def datanet_vpc(self):
        return self.__dataNet

    @property
    def website_vpc(self):
        return self.__website

    @property
    def corpnet_vpc(self):
        return self.__corpNet