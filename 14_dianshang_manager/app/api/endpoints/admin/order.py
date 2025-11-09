from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from core import dependencies
from models.user import User
from models.order import Order
from models.order_item import OrderItem
from schemas.order import Order as OrderSchema, AdminOrderList, AdminOrderUpdate

router = APIRouter()


@router.get("/orders", response_model=List[AdminOrderList])
async def getAllOrders(current_user: User = Depends(dependencies.get_admin_user)):
    orders = await Order.filter(is_deleted=False).values(
        "id", "user_id", "total_amount", "status", "created_at", "updated_at"
    )
    response_data = []
    user_id_name = {}
    for order in orders:
        # print(type(order))
        user_id = order["user_id"]
        if user_id_name.get(user_id, None) is None:
            user = await User.get_or_none(id=user_id)
            if not user:
                raise HTTPException(status_code=400, detail=f"用户：{user_id} 不存在")
            user_id_name[user_id] = user.username

        order["user_name"] = user_id_name[user_id]
        response_data.append(order)

    # print(orders)
    return response_data


@router.get("/orders/{order_id}", response_model=OrderSchema)
async def getOneOrder(
    order_id: int, current_user: User = Depends(dependencies.get_admin_user)
):
    order = await Order.get_or_none(id=order_id, is_deleted=False)
    if not order:
        raise HTTPException(status_code=400, detail="订单不存在")

    order_items = await OrderItem.filter(order_id=order_id).prefetch_related("product")
    response_data = dict(order)
    response_data["items"] = []
    for item in order_items:
        response_data["items"].append(
            {
                "product_name": item.product.name,
                "quantity": item.quantity,
                "price": item.price,
            }
        )

    # print(response_data)
    return response_data


@router.delete("/orders/{order_id}")
async def deleteOrder(
    order_id: int, current_user: User = Depends(dependencies.get_admin_user)
):
    order = await Order.get_or_none(id=order_id, is_deleted=False)
    if not order:
        raise HTTPException(status_code=400, detail="订单不存在")

    order.is_deleted = True
    order.deleted_at = datetime.now()
    await order.save()
    return dict(order_id=order_id)


@router.put("/orders/{order_id}")
async def updateOrder(
    order_id: int,
    order_data: AdminOrderUpdate,
    current_user: User = Depends(dependencies.get_admin_user),
):
    order = await Order.get_or_none(id=order_id, is_deleted=False)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    order.status = order_data.status
    order = await order.save()
    return order
