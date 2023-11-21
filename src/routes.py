from fastapi import APIRouter
from src.endpoints import check_form

router = APIRouter()

router.include_router(check_form.router)
