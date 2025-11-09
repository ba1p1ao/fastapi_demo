from fastapi import APIRouter
from api.endpoint import moive, category, auth_user, user, comment


api_router = APIRouter()

api_router.include_router(auth_user.router, prefix="/auth", tags=["auth_user"])
api_router.include_router(moive.router, prefix="/movies", tags=["movie"])
api_router.include_router(category.router, prefix="/categories", tags=["category"])
api_router.include_router(user.router, prefix="/users", tags=["user"])
api_router.include_router(comment.router, prefix="/comments", tags=["comment"])

