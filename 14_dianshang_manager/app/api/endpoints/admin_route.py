from fastapi import APIRouter
from api.endpoints.admin import order, product, user, stats

admin_router = APIRouter()

admin_router.include_router(product.router, tags=["管理商品"])
admin_router.include_router(order.router, tags=["管理订单"])
admin_router.include_router(user.router, tags=["管理用户"])
admin_router.include_router(stats.router, tags=["管理数据统计"])