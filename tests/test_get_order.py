import allure

from base.order_base import OrderBase
from data import TextResponse, IngredientsData


class TestGetUserOrders:
    """Тесты получения заказов пользователя /api/orders."""

    @allure.title('Проверка успешного получения списка заказов пользователя, код 200')
    def test_successful_get_user_orders_code_200(self, new_user):
        """Args:
            new_user (dict): данные пользователя и токены: {"user_body": dict, "token": str, "refresh_token": str}"""
        token = new_user["token"]
        body = IngredientsData.INGREDIENTS_BODY

        create_resp = OrderBase.create_order(body, token)
        assert create_resp.status_code == 200

        response = OrderBase.get_user_orders(token)
        assert response.status_code == 200 and len(response.json()["orders"]) == 1

    @allure.title('Проверка ошибки 401 при запросе списка заказов пользователя без авторизации')
    def test_failed_get_user_orders_unauthorized_code_401(self, new_user):
        """Args:
            new_user (dict): данные пользователя и токены"""
        token = new_user["token"]
        OrderBase.create_order(IngredientsData.INGREDIENTS_BODY, token)

        response = OrderBase.get_user_orders(token="")
        assert response.status_code == 401 and response.text == TextResponse.UNAUTHORIZED_USER
