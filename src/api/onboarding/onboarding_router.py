from fastapi import APIRouter,Depends
from uuid import UUID
from src.api.onboarding.services import aws_ob_router
router = APIRouter()
router.include_router(aws_ob_router,prefix='/aws',tags=['aws'])
