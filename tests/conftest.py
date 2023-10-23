import pytest
import typing
import pydantic


@pytest.fixture
def pydantic_class():
    class Item(pydantic.BaseModel):
        name: str
        price: typing.Optional[float] = None
        is_offer: bool

    return Item
