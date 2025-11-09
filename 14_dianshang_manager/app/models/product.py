from tortoise.models import Model
from tortoise import fields

class Product(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, null=False)
    description = fields.TextField(null=True)
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    stock = fields.IntField(default=0)
    category = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "products"