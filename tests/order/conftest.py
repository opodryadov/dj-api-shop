import pytest
from model_bakery import baker


@pytest.fixture
def order_factory():

    def factory(**kwargs):

        order = baker.make("Order", **kwargs)
        return order

    return factory
