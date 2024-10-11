from fastapi import APIRouter

from api.endpoints import monitoring_router, user_router

main_router = APIRouter()

main_router.include_router(monitoring_router)
main_router.include_router(user_router)
