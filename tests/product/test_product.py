import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from product.models import Product

URL = reverse("products-list")
NAME = ['Samsung Galaxy X Edge', 'iPhone X']
DESCRIPTION = ['Наконец, с нормальной батареей', '256GB']
PRICE = [65000, 80000]


@pytest.mark.django_db
def test_list_product(unauthorized_client):
    # просмотр товаров
    resp = unauthorized_client.get(URL)
    assert resp.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_create_product_by_user(api_client):
    # создать товар пользователем без прав администратора
    resp = api_client.post(URL, {
        'name': NAME[0],
        'description': DESCRIPTION[0],
        'price': PRICE[0],
    })
    assert resp.status_code == HTTP_403_FORBIDDEN
    assert Product.objects.count() == 0


@pytest.mark.django_db
def test_create_product_by_admin(admin_api_client):
    # создать товар администратором
    resp = admin_api_client.post(URL, {
        'name': NAME[0],
        'description': DESCRIPTION[0],
        'price': PRICE[0],
    })
    resp_json = resp.json()
    assert resp.status_code == HTTP_201_CREATED
    assert Product.objects.count() == 1
    assert resp_json['name'] == NAME[0]
    return resp_json


@pytest.mark.django_db
def test_update_product_by_user(api_client, admin_api_client):
    # обновить товар пользователем без прав администратора
    resp_json = test_create_product_by_admin(admin_api_client)
    url = reverse("products-detail", args=[resp_json["id"]])
    resp = api_client.patch(url, {
        'name': NAME[1],
        'description': DESCRIPTION[1],
        'price': PRICE[1],
    })
    assert resp.status_code == HTTP_403_FORBIDDEN
    assert resp_json["name"] == NAME[0]


@pytest.mark.django_db
def test_update_product_by_admin(admin_api_client):
    # обновить товар администратором
    resp_json = test_create_product_by_admin(admin_api_client)
    url = reverse("products-detail", args=[resp_json["id"]])
    resp = admin_api_client.patch(url, {
        'name': NAME[1],
        'description': DESCRIPTION[1],
        'price': PRICE[1],
    })
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert resp_json["name"] == NAME[1]


@pytest.mark.django_db
def test_delete_product_by_user(api_client, admin_api_client):
    # удалить товар пользователем без прав администратора
    resp_json = test_create_product_by_admin(admin_api_client)
    url = reverse("products-detail", args=[resp_json["id"]])
    resp = api_client.delete(url)
    assert resp.status_code == HTTP_403_FORBIDDEN
    assert Product.objects.count() == 1


@pytest.mark.django_db
def test_delete_product_by_admin(admin_api_client):
    # удалить товар администратором
    resp_json = test_create_product_by_admin(admin_api_client)
    url = reverse("products-detail", args=[resp_json["id"]])
    resp = admin_api_client.delete(url)
    assert resp.status_code == HTTP_204_NO_CONTENT
    assert Product.objects.count() == 0
