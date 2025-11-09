from fastapi import APIRouter
from api.endpoint import files, auth_user, users


api_router = APIRouter()

api_router.include_router(files.router, prefix="/files", tags=["files"])
api_router.include_router(auth_user.router, prefix="/auth", tags=["auth_user"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
