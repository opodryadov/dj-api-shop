import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from collection.models import Collection

URL = reverse("product-collections-list")


@pytest.mark.django_db
def test_list_product(unauthorized_client):
    # просмотр коллекций
    resp = unauthorized_client.get(URL)
    assert resp.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_create_collection_by_user(api_client, admin_api_client, product_factory):
    # создать коллекцию товаров пользователем
    products = product_factory(_quantity=3)
    resp = api_client.post(URL, {
        "title": "Мобильники! Налетай!",
        "text": "Подборка мобильников только для тебя!",
        "collections": [{
            "product_id": products[0].id
        },
            {
            "product_id": products[1].id
            }
        ]}, format='json')
    assert resp.status_code == HTTP_403_FORBIDDEN
    assert Collection.objects.count() == 0


@pytest.mark.django_db
def test_create_collection_by_admin(admin_api_client, product_factory):
    # создать коллекцию товаров админом
    products = product_factory(_quantity=3)
    resp = admin_api_client.post(URL, {
        "title": "Мобильники! Налетай!",
        "text": "Подборка мобильников только для тебя!",
        "collections": [{
            "product_id": products[0].id
        },
        {
            "product_id": products[1].id
        }
        ]}, format='json')
    resp_json = resp.json()
    assert resp.status_code == HTTP_201_CREATED
    assert Collection.objects.count() == 1
    return resp_json


@pytest.mark.django_db
def test_update_collection(api_client, admin_api_client, product_factory):
    # обновить коллекцию товаров пользователем/админом
    resp_json = test_create_collection_by_admin(admin_api_client, product_factory)
    url = reverse("product-collections-detail", args=[resp_json["id"]])
    product = product_factory()
    resp = api_client.patch(url, {
        "collections": [{
            "product_id": product.id
        },
        ]})
    assert resp.status_code == HTTP_403_FORBIDDEN
    resp = admin_api_client.patch(url, {
        "collections": [{
            "product_id": product.id
        },
        ]})
    assert resp.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_delete_collection(api_client, admin_api_client, product_factory):
    # удалить коллекцию товаров пользователем/админом
    resp_json = test_create_collection_by_admin(admin_api_client, product_factory)
    url = reverse("product-collections-detail", args=[resp_json["id"]])
    resp = api_client.delete(url)
    assert resp.status_code == HTTP_403_FORBIDDEN
    resp = admin_api_client.delete(url)
    assert resp.status_code == HTTP_204_NO_CONTENT
    assert Collection.objects.count() == 0
