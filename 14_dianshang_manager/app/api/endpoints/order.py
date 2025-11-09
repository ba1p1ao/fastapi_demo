from datetime import datetime
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from typing import Any, List, Dict
from tortoise.transactions import in_transaction
from tortoise.expressions import Q
from schemas.order import (
    Order as OrderSchema,
    OrderCreate,
    OrderInDB,
    OrderItemBase,
    OrderItemInDB,
)
from core import dependencies
from models.user import User
from models.order import Order
from models.product import Product
from models.order_item import OrderItem

router = APIRouter()


@router.get("/orders/my", response_model=List[OrderInDB])
async def getMyOrders(current_user: User = Depends(dependencies.get_current_user)):
    orders = await Order.filter(user=current_user, is_deleted=False)
    return orders
 

@router.post("/orders")
async def addOrder(
    order_data: OrderCreate, current_user: User = Depends(dependencies.get_current_user)
):
    async with in_transaction():
        total_amount = Decimal("0")
        order_items = []

        # 验证商品和库存
        for item in order_data.items:
            # print(item)
            product = await Product.filter(id=item.product_id).first()
            # print(list(product))
            if not product:
                raise HTTPException(
                    status_code=400, detail=f"商品ID {item.product_id} 不存在"
                )

            if item.quantity > product.stock:
                raise HTTPException(
                    status_code=400,
                    detail=f"商品 '{product.name}' 库存不足，当前库存: {product.stock}",
                )
            
            item_total = Decimal(str(item.price)) * item.quantity
            total_amount += item_total

            order_items.append(
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price": Decimal(str(item.price)),
                }
            )

        # 创建订单
        order = await Order.create(user_id=current_user.id, total_amount=total_amount)

        # 创建订单项并更新库存
        for order_item_data in order_items:
            # 创建订单项
            await OrderItem.create(order_id=order.id, **order_item_data)

            # 更新库存
            product = await Product.filter(id=order_item_data["product_id"]).first()
            product.stock -= order_item_data["quantity"]
            product.save()

        # 返回创建的订单
        return await getMyOrders(current_user)

@router.get("/orders/stats")
async def getStats(current_user: User = Depends(dependencies.get_current_user)):
    order_count = await Order.filter(user_id=current_user.id, is_deleted=False).count()
    order_pending_count = await Order.filter(user_id=current_user.id, is_deleted=False, status="pending").count()
    order_success_count = await Order.filter(user_id=current_user.id, is_deleted=False, status="completed").count()
    order_cancel_count = await Order.filter(user_id=current_user.id, is_deleted=False, status="cancelled").count()
    order_total_amount = Decimal("0")
    orders = await Order.filter((Q(user_id=current_user.id) & Q(status="completed") & Q(is_deleted=False)))
    for order in orders:
        if order.status == "completed":
            order_total_amount += Decimal(str(order.total_amount))
    response_data = {
        "total_orders": order_count,
        "pending_orders": order_pending_count,
        "completed_orders": order_success_count,
        "cancelled_orders": order_cancel_count,
        "total_spent": order_total_amount
    }
    # print(response_data)
    return response_data



@router.get("/orders/{order_id}", response_model=OrderSchema)
async def getOneOrder(
    order_id: int, current_user: User = Depends(dependencies.get_current_user)
):
    order = await Order.get_or_none(id=order_id, user_id=current_user.id, is_deleted=False)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    order_items = await OrderItem.filter(order=order).prefetch_related("product")
    order_data = dict(order)
    order_data["items"] = []
    # print(order_data)
    for order_item in order_items:
        order_data["items"].append(
            {
                "product_name": order_item.product.name,
                "quantity": order_item.quantity,
                "price": order_item.price,
            }
        )
        # print(order_data["items"])

    return order_data


@router.put("/orders/{order_id}/cancel")
async def updateOrder(order_id: int, current_user: User = Depends(dependencies.get_current_user)):
    order = await Order.get_or_none(id=order_id, user=current_user, is_deleted=False)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    if order.status != "pending":
        raise HTTPException(status_code=400, detail="只能取消待处理的订单")
    
    async with in_transaction():
        order.status = "cancelled"
        await order.save()

        order_items = await OrderItem.filter(order_id=order.id)
        for item in order_items:
            # print(list(item))
            # print(item.quantity)
            product = await Product.filter(id=item.product_id).first()
            product.stock += item.quantity
            await product.save()

    return await getMyOrders(current_user)


@router.delete("/orders/{order_id}/delete")
async def deleteOrder(order_id: int, current_user: User = Depends(dependencies.get_current_user)):
    order = await Order.get_or_none(id=order_id, user=current_user, is_deleted=False)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    if order.status != "cancelled":
        raise HTTPException(status_code=400, detail="只能删除已取消的订单")
    
    async with in_transaction():
        await Order.filter(id=order_id, user=current_user).update(is_deleted=True, deleted_at=datetime.now())

    return await getMyOrders(current_user)

