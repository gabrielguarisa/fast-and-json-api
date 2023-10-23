import pydantic
import typing


class Item(pydantic.BaseModel):
    name: str
    price: typing.Optional[float] = None
    is_offer: bool


import pydantic2jsonapi as p2j

JsonApiItem = p2j.to_jsonapi(Item)

item = JsonApiItem(**{"data": {"attributes": {"name": "Foo", "is_offer": True}}})

print(item.model_dump())


JsonApiManyItems = p2j.to_jsonapi(Item, many=True)

items = JsonApiManyItems(
    **{
        "data": [
            {"attributes": {"name": "Foo", "is_offer": True}},
            {"attributes": {"name": "Foo", "price": 100, "is_offer": False}},
        ]
    }
)

print(items.model_dump())
