# pydantic2jsonapi

A minimalistic library to convert Pydantic models to JSON:API compliant.

## Installation

```bash
pip install pydantic2jsonapi
```

## Why?

In my current workplace we use [JSON:API](https://jsonapi.org/) specification to communicate between our apps. The problem is that when we want to use simple [pydantic](https://docs.pydantic.dev/latest/) models to validate our data, we need to write a lot of boilerplate code to convert pydantic models to JSON:API format. This library aims to solve this problem.

## Usage

Let's say we have a simple pydantic model:

```python
import pydantic
import typing

class Item(pydantic.BaseModel):
    name: str
    price: typing.Optional[float] = None
    is_offer: bool
```

To convert this model class to JSON:API format, you just need to call this function:

```python
import pydantic2jsonapi as p2j

JsonApiItem = p2j.to_jsonapi(Item)
```

Now you can use `JsonApiItem` class to validate your data and convert it to JSON:API format:

```python
item = JsonApiItem(**{"data": {"attributes": {"name": "Foo", "is_offer": True}}})

print(item.model_dump())
# {'data': {'type_': 'item', 'attributes': {'name': 'Foo', 'price': None, 'is_offer': True}}}
```

If you want to skip the `data.attributes` part, you can use the class method `from_original_instance`:

```python
item = JsonApiItem.from_original_instance(Item(name="Foo", is_offer=True))
```

Or if you want to pass the attributes directly to the constructor, you can use the class method `from_dict_instance`:

```python
item = JsonApiItem.from_dict_instance(**{"name": "Foo", "is_offer": True})
```

### List of models

If you want to create a JSON:API model that represents a list of models, you can use the `to_jsonapi` function with the `many` parameter set to `True`:

```python
JsonApiManyItems = p2j.to_jsonapi(Item, many=True)
```

Now you can use `JsonApiManyItems` class to validate your data and convert it to JSON:API format:

```python
items = JsonApiManyItems(
    **{
        "data": [
            {"attributes": {"name": "Foo", "is_offer": True}},
            {"attributes": {"name": "Foo", "price": 100, "is_offer": False}},
        ]
    }
)

print(items.model_dump())
# {'data': [{'type_': 'item', 'attributes': {'name': 'Foo', 'price': None, 'is_offer': True}}, {'type_': 'item', 'attributes': {'name': 'Foo', 'price': 100.0, 'is_offer': False}}]}
```

## Alternatives

- [pydantic-jsonapi](https://pypi.org/project/pydantic-jsonapi/)
- [FastAPI-JSONAPI](https://pypi.org/project/FastAPI-JSONAPI/)