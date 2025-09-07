from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator  # type: ignore


class Item(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=100)


ItemSchema = pydantic_model_creator(Item)
ItemCreate = pydantic_model_creator(Item, exclude_readonly=True)
