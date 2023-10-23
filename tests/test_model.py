import pytest
import pydantic2jsonapi as p2j


@pytest.mark.parametrize(
    "conversion_kwargs,input_dict, expected_dict",
    [
        (
            {},
            {"name": "example", "price": 100, "is_offer": True},
            {
                "data": {
                    "type_": "item",
                    "attributes": {"name": "example", "price": 100.0, "is_offer": True},
                }
            },
        ),
        (
            {"type_to_lowercase": False},
            {"name": "example", "price": 100, "is_offer": True},
            {
                "data": {
                    "type_": "Item",
                    "attributes": {"name": "example", "price": 100.0, "is_offer": True},
                }
            },
        ),
        (
            {"default_type_value": "test_type_value"},
            {"name": "example", "price": 100, "is_offer": True},
            {
                "data": {
                    "type_": "test_type_value",
                    "attributes": {"name": "example", "price": 100.0, "is_offer": True},
                }
            },
        ),
    ],
)
def test_jsonapi_model_from_original_instance(
    pydantic_class, conversion_kwargs, input_dict, expected_dict
):
    jsonapi_class = p2j.to_jsonapi(pydantic_class, **conversion_kwargs)

    jsonapi_instance = jsonapi_class.from_original_instance(input_dict)

    assert jsonapi_instance.model_dump() == expected_dict
    assert jsonapi_instance.get_original_instance() == pydantic_class(**input_dict)


def test_jsonapi_model_with_many(pydantic_class):
    jsonapi_class = p2j.to_jsonapi(pydantic_class, many=True)

    jsonapi_instance = jsonapi_class(
        **{
            "data": [
                {
                    "type_": "item",
                    "attributes": {"name": "example", "price": 100.0, "is_offer": True},
                },
                {
                    "type_": "item",
                    "attributes": {"name": "test2", "price": 0, "is_offer": False},
                },
            ]
        }
    )

    assert isinstance(jsonapi_instance, jsonapi_class)
    assert isinstance(jsonapi_instance.data, list)
    assert len(jsonapi_instance.data) == 2

    assert jsonapi_instance.data[0].type_ == "item"
    assert jsonapi_instance.data[0].attributes.name == "example"

    assert jsonapi_instance.data[1].type_ == "item"
    assert jsonapi_instance.data[1].attributes.name == "test2"


@pytest.mark.parametrize(
    "instance_input, expected_dict, expected_length",
    [
        (
            [
                {"name": "example", "price": 100, "is_offer": True},
                {"name": "test2", "price": 0, "is_offer": False},
            ],
            {
                "data": [
                    {
                        "type_": "item",
                        "attributes": {
                            "name": "example",
                            "price": 100.0,
                            "is_offer": True,
                        },
                    },
                    {
                        "type_": "item",
                        "attributes": {
                            "name": "test2",
                            "price": 0.0,
                            "is_offer": False,
                        },
                    },
                ]
            },
            2,
        ),
        (
            {"name": "example", "price": 100, "is_offer": True},
            {
                "data": [
                    {
                        "type_": "item",
                        "attributes": {
                            "name": "example",
                            "price": 100.0,
                            "is_offer": True,
                        },
                    }
                ]
            },
            1,
        ),
    ],
)
def test_jsonapi_model_with_many_from_original_instance(
    pydantic_class, instance_input, expected_dict, expected_length
):
    jsonapi_class = p2j.to_jsonapi(pydantic_class, many=True)

    jsonapi_instance = jsonapi_class.from_original_instance(instance_input)

    assert isinstance(jsonapi_instance, jsonapi_class)
    assert isinstance(jsonapi_instance.data, list)
    assert len(jsonapi_instance.data) == expected_length

    print(jsonapi_instance.model_dump())
    assert jsonapi_instance.model_dump() == expected_dict

def test_jsonapi_model_from_dict_instance(pydantic_class):
    jsonapi_class = p2j.to_jsonapi(pydantic_class)

    jsonapi_instance = jsonapi_class.from_dict_instance(
        **{"name": "example", "price": 100.0, "is_offer": True}
    )

    assert isinstance(jsonapi_instance, jsonapi_class)
    assert jsonapi_instance.data.type_ == "item"
    assert jsonapi_instance.data.attributes.name == "example"
    assert jsonapi_instance.data.attributes.price == 100.0
    assert jsonapi_instance.data.attributes.is_offer == True