import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_201_CREATED, HTTP_204_NO_CONTENT, \
    HTTP_401_UNAUTHORIZED
from django.contrib.auth.models import User
from order.models import Order
from tests.product.test_product import test_create_product_by_admin

URL = reverse("orders-list")


@pytest.mark.django_db
def test_create_order_by_unauthorized(api_client, admin_api_client):
    # создать заказ пользователем
    product_json = test_create_product_by_admin(admin_api_client)
    resp = api_client.post(URL, {
        "positions": [
            {
                "product_id": product_json['id'],
                "quantity": 10,
            }
        ]
    })
    assert resp.status_code == HTTP_201_CREATED
    assert Order.objects.count() == 1


@pytest.mark.django_db
def test_order_list(api_client, admin_api_client, order_factory):
    # администраторы могут получать все заказы, пользователи - только свои
    admin_quantity, user_quantity = 2, 3
    order_factory(creator=User.objects.get(username='user'), _quantity=user_quantity)
    order_factory(creator=User.objects.get(username='admin'), _quantity=admin_quantity)
    resp = api_client.get(URL)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert len(resp_json) == user_quantity
    resp = admin_api_client.get(URL)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert len(resp_json) == (admin_quantity + user_quantity)


@pytest.mark.django_db
def test_create_order_by_unauthorized(unauthorized_client, admin_api_client):
    # создать заказ неавторизированным пользователем
    product_json = test_create_product_by_admin(admin_api_client)
    resp = unauthorized_client.post(URL, {
        "positions": [
            {
                "product_id": product_json['id'],
                "quantity": 10
            }
        ]
    })
    assert resp.status_code == HTTP_401_UNAUTHORIZED
    assert Order.objects.count() == 0


@pytest.mark.django_db
def test_update_order(api_client, admin_api_client, order_factory):
    # изменить статус заказа пользователем/админом
    order = order_factory(creator=User.objects.get(username='user'))
    url = reverse("orders-detail", args=[order.id])
    resp = api_client.patch(url, {
        "status": "IN_PROGRESS"
    })
    assert resp.status_code == HTTP_403_FORBIDDEN
    resp = admin_api_client.patch(url, {
        "status": "IN_PROGRESS"
    })
    assert resp.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_delete_order_by_user(api_client, admin_api_client, order_factory):
    # удалить заказ пользователем/админом
    order = order_factory(creator=User.objects.get(username='user'))
    url = reverse("orders-detail", args=[order.id])
    resp = api_client.delete(url)
    assert resp.status_code == HTTP_403_FORBIDDEN
    resp = admin_api_client.delete(url)
    assert resp.status_code == HTTP_204_NO_CONTENT
