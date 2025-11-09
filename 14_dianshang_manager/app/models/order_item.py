from tortoise.models import Model
from tortoise import fields

class OrderItem(Model):
    id = fields.IntField(pk=True)
    order = fields.ForeignKeyField("models.Order", related_name="order_items")
    product = fields.ForeignKeyField("models.Product", related_name="order_items")
    quantity = fields.IntField()
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "order_items"