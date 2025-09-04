import allure

from base.order_base import OrderBase
from data import TextResponse, IngredientsData


class TestCreateOrders:
    """
    Тесты создания заказа /api/orders.
    """

    @allure.title('Проверка успешного создания заказа, код 200')
    def test_successful_create_order_code_200(self, new_user):
        """
        Args:
            new_user (dict): данные пользователя и токены: {"user_body": dict, "token": str, "refresh_token": str}
        """
        token = new_user['token']
        body = IngredientsData.INGREDIENTS_BODY
        response = OrderBase.create_order(body, token)
        assert response.status_code == 200 and response.json()['success'] is True

    @allure.title('Проверка ошибки 401 при создании заказа без авторизации')
    def test_failed_create_order_unauthorized_code_401(self):
        body = IngredientsData.INGREDIENTS_BODY
        response = OrderBase.create_order(body, token=None)
        assert response.status_code == 401 and response.text == TextResponse.UNAUTHORIZED_USER

    @allure.title('Проверка ошибки 400 при создании заказа без ингредиентов')
    def test_failed_create_order_no_ingredients_code_400(self, new_user):
        """
        Args:
            new_user (dict): данные пользователя и токены
        """
        token = new_user['token']
        body = {}  # отсутствует ключ "ingredients"
        response = OrderBase.create_order(body, token)
        assert response.status_code == 400 and response.text == TextResponse.NO_INGREDIENTS

    @allure.title('Проверка ошибки 500 при некорректном ID ингредиента')
    def test_failed_create_order_incorrect_ingredients_code_500(self, new_user):
        """
        Args:
            new_user (dict): данные пользователя и токены
        """
        token = new_user['token']
        body = IngredientsData.INVALID_INGREDIENTS_BODY
        response = OrderBase.create_order(body, token)
        assert response.status_code == 500