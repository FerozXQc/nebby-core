from fastapi import APIRouter,Depends
from uuid import UUID
from src.core.integration import generate_aws_stack_url
from src.api.routers.auth_router import get_current_user
from src.utils.aws_helpers import get_boto3_client
router = APIRouter()

@router.get("/aws-onboarding")
def generate_aws_onboarding_url(bucket_name:str,external_id:UUID,region='us-east-1',expires_in=3600, user=Depends(get_current_user)):
    return generate_aws_stack_url(bucket_name,region,expires_in,external_id=user.id)
