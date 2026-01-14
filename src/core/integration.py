import json
from src.utils.aws_helpers import get_boto3_client
import os
from dotenv import load_dotenv
from uuid import UUID
import urllib.parse

load_dotenv()

def generate_onboarding_template(external_id: UUID):
    return json.dumps({
        "AWSTemplateFormatVersion": "2010-09-09",
        "Description": "Nebby AWS Read-Only Access Role",
        "Resources": {
            "NebbyRole": {
                "Type": "AWS::IAM::Role",
                "Properties": {
                    "RoleName": "NebbyReadOnlyRole",
                    "AssumeRolePolicyDocument": {
                        "Version": "2012-10-17",
                        "Statement": [{
                            "Effect": "Allow",
                            "Principal": {
                                "AWS": f"arn:aws:iam::{os.getenv('NEBBY_ACCOUNT_ID')}:root"
                            },
                            "Action": "sts:AssumeRole",
                            "Condition": {
                                "StringEquals": {
                                    "sts:ExternalId": external_id
                                }
                            }
                        }]
                    },
                    "ManagedPolicyArns": [
                        "arn:aws:iam::aws:policy/ReadOnlyAccess"
                    ]
                }
            }
        },
        "Outputs": {
            "RoleArn": {
                "Description": "Role ARN to provide to Nebby",
                "Value": {"Fn::GetAtt": ["NebbyRole", "Arn"]}
            }
        }
    })

def upload_onboarding_template(template_json:str,external_id:UUID,s3_client)->str:
    key = f"/templates/aws_onboarding/{external_id},json",
    s3_client.put_object(
        Bucket = os.getenv('onboarding-bucket-name'),
        Key = key, 
        Body=template_json,
        ContentType='application/json',
    )
    return key

def get_presigned_url_template(key:str,s3_client,expires_in)->str:
    return s3_client.generate_presigned_url(
        ClientMethod='get-method',
        Params={
            "Bucket":os.getend('onboarding-bucket-name'),
            "Key":key
        },
        Expires_in=expires_in
    )

def generate_launch_stack_url(template_url: str, region="us-east-1")->str:
    base = "https://console.aws.amazon.com/cloudformation/home"
    params = {
        "region": region,
        "templateURL": template_url
    }
    return f"{base}#/stacks/create/review?{urllib.parse.urlencode(params)}"

def generate_aws_stack_url(bucket_name:str,external_id:UUID,region='us-east-1',expires_in=3600):
    s3_client = get_boto3_client('s3')
    template_json = generate_onboarding_template(external_id)
    template_key = upload_onboarding_template(template_json,external_id,s3_client)
    template_url = get_presigned_url_template(template_key,s3_client,expires_in)
    return generate_launch_stack_url(template_url,region)
