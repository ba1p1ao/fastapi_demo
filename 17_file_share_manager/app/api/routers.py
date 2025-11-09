from fastapi import APIRouter
from api.endpoint import auth_user, file, user

router = APIRouter()

router.include_router(auth_user.router, prefix="/auth", tags=["auth user"])
router.include_router(file.router, prefix="/files", tags=["files"])
router.include_router(user.router, prefix="/users", tags=["users"])