import json
from src.utils.aws_helpers import get_boto3_client
import os
from dotenv import load_dotenv
import uuid
load_dotenv()

def generate_onboarding_template(external_id: uuid):
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

