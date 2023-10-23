import pydantic
import pydantic2jsonapi as p2j


def test_create_jsonapi_data_wrapper_class(pydantic_class):
    jsonapi_model = p2j.create_data_wrapper(pydantic_class)
    assert isinstance(jsonapi_model, type)
    assert issubclass(jsonapi_model, pydantic.BaseModel)
    assert jsonapi_model.__name__ == "ItemDataWrapper"
    assert jsonapi_model.model_json_schema() == {
        "$defs": {
            "Item": {
                "properties": {
                    "name": {"title": "Name", "type": "string"},
                    "price": {
                        "anyOf": [{"type": "number"}, {"type": "null"}],
                        "default": None,
                        "title": "Price",
                    },
                    "is_offer": {"title": "Is Offer", "type": "boolean"},
                },
                "required": ["name", "is_offer"],
                "title": "Item",
                "type": "object",
            }
        },
        "properties": {
            "type": {"default": "item", "title": "Type", "type": "string"},
            "attributes": {"$ref": "#/$defs/Item"},
        },
        "required": ["attributes"],
        "title": "ItemDataWrapper",
        "type": "object",
    }


def test_pydantic_to_jsonapi_wrapper_class(pydantic_class):
    jsonapi_model = p2j.to_jsonapi(pydantic_class)
    assert isinstance(jsonapi_model, type)
    assert issubclass(jsonapi_model, pydantic.BaseModel)
    assert jsonapi_model.__name__ == "ItemWrapper"

    assert jsonapi_model.model_json_schema() == {
        "$defs": {
            "DataWrapper": {
                "properties": {
                    "type": {"default": "item", "title": "Type", "type": "string"},
                    "attributes": {"$ref": "#/$defs/Item"},
                },
                "required": ["attributes"],
                "title": "ItemDataWrapper",
                "type": "object",
            },
            "Item": {
                "properties": {
                    "name": {"title": "Name", "type": "string"},
                    "price": {
                        "anyOf": [{"type": "number"}, {"type": "null"}],
                        "default": None,
                        "title": "Price",
                    },
                    "is_offer": {"title": "Is Offer", "type": "boolean"},
                },
                "required": ["name", "is_offer"],
                "title": "Item",
                "type": "object",
            },
        },
        "properties": {"data": {"$ref": "#/$defs/DataWrapper"}},
        "required": ["data"],
        "title": "ItemWrapper",
        "type": "object",
    }


def test_many_pydantic_to_jsonapi_wrapper_class(pydantic_class):
    jsonapi_model = p2j.to_jsonapi(pydantic_class, many=True)

    assert isinstance(jsonapi_model, type)
    assert issubclass(jsonapi_model, pydantic.BaseModel)
    assert jsonapi_model.__name__ == "ManyItemWrapper"

    assert jsonapi_model.model_json_schema() == {
        "$defs": {
            "DataWrapper": {
                "properties": {
                    "type": {"default": "item", "title": "Type", "type": "string"},
                    "attributes": {"$ref": "#/$defs/Item"},
                },
                "required": ["attributes"],
                "title": "ItemDataWrapper",
                "type": "object",
            },
            "Item": {
                "properties": {
                    "name": {"title": "Name", "type": "string"},
                    "price": {
                        "anyOf": [{"type": "number"}, {"type": "null"}],
                        "default": None,
                        "title": "Price",
                    },
                    "is_offer": {"title": "Is Offer", "type": "boolean"},
                },
                "required": ["name", "is_offer"],
                "title": "Item",
                "type": "object",
            },
        },
        "properties": {
            "data": {
                "items": {"$ref": "#/$defs/DataWrapper"},
                "title": "Data",
                "type": "array",
            }
        },
        "required": ["data"],
        "title": "ManyItemWrapper",
        "type": "object",
    }
