import boto3

def get_boto3_client(service_name: str):
    return boto3.client(service_name)