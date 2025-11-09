from fastapi import APIRouter, HTTPException
from typing import List, Optional
from tortoise.expressions import Q
from models.product import Product
from schemas.product import ProductInDB, Categorie


router = APIRouter()


@router.get("/products", response_model=List[ProductInDB])
async def getAllProducts(
    q: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
):

    # args = {
    #     "name__icontains": q,
    #     "description__icontains": q,
    #     "category__icontains": category,
    #     "price__gt": min_price,
    #     "price__lt": max_price,
    # }
    # args_ignore_none = {k: v for k, v in args.items() if v is not None}
    # # print(args_ignore_none)
    # products = await Product.filter(**args_ignore_none).all()
    # print(q)
    # print(products)

    products = Product.all()
    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))
    if category:
        products = products.filter(Q(category__icontains=category))
    if min_price is not None:
        products = products.filter(price__gte=min_price)
    if max_price is not None:
        products = products.filter(price__lte=max_price)

    # 查看生成的SQL
    # sql_query = str(products.sql())
    # print(f"Generated SQL: {sql_query}")

    products = await products
    return products

@router.get("/products/categories", response_model=Categorie)
async def getCategories():
    categories = await Product.all().values("category")
    # print(categories)
    category_set = set()
    for cate in categories:
        category_set.add(cate["category"])

    response_data = {"categories": list(category_set)}

    return response_data

@router.get("/products/{product_id}", response_model=ProductInDB)
async def getOneProduct(product_id: int):
    product = await Product.get_or_none(id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")

    return product


