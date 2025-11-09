from fastapi import APIRouter
from api.endpoints import user, product, order, admin_route


api_router = APIRouter()

api_router.include_router(user.router, tags=["用户管理"])
api_router.include_router(product.router, tags=["商品管理"])
api_router.include_router(order.router, tags=["订单管理"])
api_router.include_router(admin_route.admin_router, prefix="/admin", tags=["管理员"])
