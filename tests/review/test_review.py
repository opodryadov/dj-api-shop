import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_201_CREATED, HTTP_204_NO_CONTENT, \
    HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST
from review.models import Review
from tests.product.test_product import test_create_product_by_admin

URL = reverse('product-reviews-list')
TEXT = ['Отличный смартфон! Советую к покупке!', 'Ужасный смартфон! Не советую!!']
RATING = [1, 2, 3, 4, 5]


@pytest.mark.django_db
def test_get_reviews(unauthorized_client):
    # просмотр отзывов
    resp = unauthorized_client.get(URL)
    assert resp.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_create_review_by_unauthorized(unauthorized_client, admin_api_client):
    # оставить отзыв неавторизированным пользователем
    product_json = test_create_product_by_admin(admin_api_client)
    resp = unauthorized_client.post(URL, {
        'product': product_json['id'],
        'text': TEXT[0],
        'rating': RATING[0],
    })
    assert resp.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_review_by_user(api_client, admin_api_client):
    # оставить отзыв авторизированным пользователем дважды
    product_json = test_create_product_by_admin(admin_api_client)
    resp = api_client.post(URL, {
        'product': product_json['id'],
        'text': TEXT[0],
        'rating': RATING[4],
    })
    resp_json = resp.json()
    assert resp.status_code == HTTP_201_CREATED
    assert Review.objects.count() == 1
    assert resp_json['product'] == product_json['id']
    assert resp_json['text'] == TEXT[0]
    resp = api_client.post(URL, {
        'product': product_json['id'],
        'text': TEXT[0],
        'rating': RATING[2],
    })
    assert resp.status_code == HTTP_400_BAD_REQUEST
    assert Review.objects.filter(product=resp_json['product']).filter(creator=resp_json['creator']['id']).count() == 1


@pytest.mark.django_db
def test_update_or_delete_someone_review(api_client, review_factory):
    # изменить или удалить чужой отзыв
    review = review_factory()
    assert Review.objects.count() == 1
    url = reverse("product-reviews-detail", args=[review.id])
    resp = api_client.patch(url, {
        'text': TEXT[1],
        'rating': RATING[1],
    })
    assert resp.status_code == HTTP_403_FORBIDDEN
    resp = api_client.delete(url)
    assert resp.status_code == HTTP_403_FORBIDDEN
    assert Review.objects.count() == 1


@pytest.mark.django_db
def test_update_own_review(api_client, admin_api_client):
    # изменить и удалить свой отзыв
    product_json = test_create_product_by_admin(admin_api_client)
    resp = api_client.post(URL, {
        'product': product_json['id'],
        'text': TEXT[0],
        'rating': RATING[0],
    })
    resp_json = resp.json()
    assert resp.status_code == HTTP_201_CREATED
    assert Review.objects.count() == 1
    assert resp_json['product'] == product_json['id']
    assert resp_json['text'] == TEXT[0]
    url = reverse("product-reviews-detail", args=[resp_json['id']])
    resp = api_client.patch(url, {
        'product': product_json['id'],
        'text': TEXT[1],
        'rating': RATING[1],
    })
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert resp_json["text"] == TEXT[1]
    resp = api_client.delete(url)
    assert resp.status_code == HTTP_204_NO_CONTENT
    assert Review.objects.count() == 0
