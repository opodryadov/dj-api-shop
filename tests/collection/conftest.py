import pytest
from model_bakery import baker


@pytest.fixture
def product_factory():

    def factory(**kwargs):

        product = baker.make("Product", **kwargs)
        return product

    return factory
