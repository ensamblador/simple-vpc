from aws_cdk import Stack, CfnOutput, aws_ec2 as ec2, aws_ssm as ssm
from constructs import Construct


class NetworkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "V", max_azs=2)
        private_subnets = vpc.private_subnets
        public_subnets = vpc.public_subnets

        private_subnets_ids = ",".join([sn.subnet_id for sn in private_subnets])
        public_subnets_ids = ",".join([sn.subnet_id for sn in public_subnets])

        self.create_ssm_param("vpc-id", vpc.vpc_id)
        self.create_ssm_param("vpc-azs", ",".join(vpc.availability_zones))
        self.create_ssm_param("vpc-private-subnets", private_subnets_ids)
        self.create_ssm_param("vpc-public-subnets", public_subnets_ids)

    def create_ssm_param(self, name, value):
        ssm.StringParameter( self, f"ssm-{name}",
            parameter_name=f"/gen-ai-apps/{name}",string_value=value)


