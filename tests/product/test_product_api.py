import pytest
from django.urls import reverse
from rest_framework.status import *
from rest_framework.authtoken.models import Token
from product.models import Product


@pytest.mark.django_db
def test_product(api_client, django_user_model):
    admin = django_user_model.objects.create_user(username='admin', password='admin', is_staff=True)
    admin_token = Token.objects.create(user=admin)
    user = django_user_model.objects.create_user(username='user', password='user')
    user_token = Token.objects.create(user=user)

    # LIST
    url = reverse("products-list")
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK  # просмотр товаров

    # CREATE
    # попытка создать товар пользователем
    name = 'Samsung Galaxy X Edge'
    description = 'Наконец, с нормальной батареей'
    price = 65000

    api_client.force_login(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_token.key}')
    resp = api_client.post(url, {
        'name': name,
        'description': description,
        'price': price
    })
    assert resp.status_code == HTTP_403_FORBIDDEN
    assert Product.objects.count() == 0

    # попытка создать товар администратором
    api_client.force_login(admin)
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {admin_token.key}')
    resp = api_client.post(url, {
        'name': name,
        'description': description,
        'price': price
    })
    resp_json = resp.json()
    assert resp.status_code == HTTP_201_CREATED
    assert Product.objects.count() == 1
    assert resp_json["name"] == name

    # UPDATE
    # попытка обновить товар пользователем
    url = reverse("products-detail", args=[resp_json["id"]])

    name = 'iPhone X'
    description = '256GB'
    price = 80000

    api_client.force_login(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_token.key}')
    resp = api_client.patch(url, {
        'name': name,
        'description': description,
        'price': price
    })
    assert resp.status_code == HTTP_403_FORBIDDEN

    # попытка обновить товар администратором
    url = reverse("products-detail", args=[resp_json["id"]])

    name = 'iPhone X'
    description = '256GB'
    price = 80000

    api_client.force_login(user=admin)
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {admin_token.key}')
    resp = api_client.patch(url, {
        'name': name,
        'description': description,
        'price': price
    })
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert resp_json["name"] == name

    # DELETE
    # попытка удалить товар пользователем
    api_client.force_login(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {user_token.key}')
    resp = api_client.delete(url)
    assert resp.status_code == HTTP_403_FORBIDDEN

    # попытка удалить товар администратором
    api_client.force_login(user=admin)
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {admin_token.key}')
    resp = api_client.delete(url)
    assert resp.status_code == HTTP_204_NO_CONTENT
    assert Product.objects.count() == 0
