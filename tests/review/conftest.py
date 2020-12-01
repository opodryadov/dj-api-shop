import pytest
from model_bakery import baker


@pytest.fixture
def review_factory():

    def factory(**kwargs):
        review = baker.make("Review", **kwargs)
        return review

    return factory
