from fastapi import APIRouter, HTTPException, Depends
from typing import List
from core import dependencies
from schemas.product import ProductBase, ProductCreate, ProductUpdate, ProductInDB
from models.user import User
from models.product import Product

router = APIRouter()


@router.get("/products")
async def getAllProduct(current_user: User = Depends(dependencies.get_admin_user)):
    products = await Product.all()
    return products

@router.get("/products/low-stock", response_model=List[ProductInDB])
async def getLowstockProduct(current_user: User = Depends(dependencies.get_admin_user)):
    products = await Product.filter(stock__lte=10)
    return products

@router.get("/products/{product_id}")
async def getOneProduct(product_id: int):
    product = await Product.get_or_none(id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")

    return product

@router.post("/products")
async def addProduct(product_data: ProductCreate, current_user: User = Depends(dependencies.get_admin_user)):
    args = {
        "name": product_data.name,
        "description": product_data.description,
        "price": product_data.price,
        "stock": product_data.stock,
        "category": product_data.category,
    }

    args_no_none = {k: v for k, v in args.items() if v is not None}

    prodect = await Product.create(**args_no_none)
    return prodect


@router.put("/products/{product_id}")
async def updateProduct(product_id: int, product_data: ProductUpdate, current_user: User = Depends(dependencies.get_admin_user)):
    product = await Product.get_or_none(id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    
    product_data = product_data.model_dump()
    product = await Product.filter(id=product_id).update(**product_data)

    return product



@router.delete("/products/{product_id}")
async def deleteProduct(product_id: int, current_user: User = Depends(dependencies.get_admin_user)):
    product = await Product.filter(id=product_id).delete()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    return product


