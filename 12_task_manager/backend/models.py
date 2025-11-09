from tortoise.models import Model
from tortoise import fields
from datetime import datetime

class Task(Model):
    id = fields.IntField(pk=True, description="task id")
    title = fields.CharField(max_length=255, description="task title")
    description = fields.CharField(max_length=255, description="task description", default="")
    is_completed = fields.BooleanField(description="task is completed", default=False)
    created_at = fields.DatetimeField(description="task create datetime")
    updated_at = fields.DatetimeField(description="task update datetime")

