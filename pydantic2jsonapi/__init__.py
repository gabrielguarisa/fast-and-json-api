import pydantic
import typing


def create_data_wrapper(
    model: typing.Type[pydantic.BaseModel],
    default_type_value: str = None,
    type_to_lowercase: bool = True,
) -> typing.Type[pydantic.BaseModel]:
    """Create a wrapper class for a pydantic model to be used as a JSON:API data object.

    :param model: The pydantic model to wrap.
    :param default_type_value: The default value for the "type" field.
    :param type_to_lowercase: If True, the "type" field will be converted to lowercase.

    :return: A pydantic model that wraps the given model.
    """
    if default_type_value is None:
        type_value = model.__name__.lower() if type_to_lowercase else model.__name__
    else:
        type_value = default_type_value

    class DataWrapper(pydantic.BaseModel):
        type_: str = pydantic.Field(type_value, alias="type")
        attributes: model

    DataWrapper.__name__ = f"{model.__name__}DataWrapper"

    return DataWrapper


def to_jsonapi(
    model: typing.Type[pydantic.BaseModel],
    many: bool = False,
    **kwargs,
) -> typing.Type[pydantic.BaseModel]:
    """Create a wrapper class for a pydantic model to be used as a JSON:API resource.

    :param model: The pydantic model to wrap.
    :param many: If True, the wrapper will be for a JSON:API collection.

    :return: A pydantic model that wraps the given model.
    """
    DataWrapper = create_data_wrapper(model, **kwargs)

    class Wrapper(pydantic.BaseModel):
        data: typing.List[DataWrapper] if many else DataWrapper

        def get_original_instance(self) -> pydantic.BaseModel:
            return self.data.attributes

        @classmethod
        def from_original_instance(cls, instance: pydantic.BaseModel) -> "Wrapper":
            if not many:
                if isinstance(instance, dict):
                    instance = model(**instance)

                return cls(data=DataWrapper(attributes=instance))

            if not isinstance(instance, list):
                instance = [instance]

            data_items = []

            for item in instance:
                if isinstance(item, dict):
                    item = model(**item)

                data_items.append(DataWrapper(attributes=item))

            return cls(data=data_items)

        @classmethod
        def from_dict_instance(self, **instance) -> "Wrapper":
            return self.from_original_instance(model(**instance))

    Wrapper.__name__ = (
        f"Many{model.__name__}Wrapper" if many else f"{model.__name__}Wrapper"
    )

    return Wrapper
