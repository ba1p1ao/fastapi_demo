from fastapi import APIRouter, HTTPException, Depends
from tortoise.expressions import Q
from typing import List
from decimal import Decimal
from core import dependencies
from models.user import User
from models.product import Product
from models.order import Order
from schemas.user import UserResponse


router = APIRouter()


@router.get("/stats")
async def getStats(current_user: User = Depends(dependencies.get_admin_user)):
    total_users = await User.filter().count()
    total_products = await Product.filter().count()
    total_orders = await Order.filter(is_deleted=False).count()
    total_revenue = Decimal("0")
    orders = await Order.filter(status="completed", is_deleted=False)
    for order in orders:
        total_revenue += Decimal(str(order.total_amount))


    response_data = {
        "total_users": total_users,
        "total_orders": total_orders,
        "total_products": total_products,
        "total_revenue": total_revenue,
    }
    # print(response_data)
    return response_data
