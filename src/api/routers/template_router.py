from fastapi import APIRouter
import uuid
router = APIRouter()

@router.get("/aws-onboarding/{external_id}.json")
def generate_onboarding_template(external_id:uuid):
    return 
