import allure
import requests

from data import Config


class OrderBase:
    """
    Базовые методы работы с эндпоинтом /api/orders для сервиса Stellar Burgers.
    """

    @staticmethod
    @allure.step('Создать заказ')
    def create_order(body: dict, token: str | None = None) -> requests.Response:
        """
        Создаёт заказ через POST /api/orders. При наличии токена запрос выполняется от имени авторизованного пользователя.
        Args:
            body (dict): Тело запроса в формате JSON. Обязательное поле — "ingredients": list[str].
            token (str | None): Строка авторизации в формате "Bearer <accessToken>". Если None — запрос выполняется без авторизации.
        Return:
            requests.Response: HTTP-ответ библиотеки requests с кодом статуса и телом ответа.
        """
        headers = {}
        if token:
            headers['Authorization'] = token  # ожидается строка вида "Bearer <accessToken>"

        return requests.post(
            f'{Config.MAIN_URL}{Config.URL_CREATE_ORDER}',
            json=body,
            headers=headers or None
        )

    @staticmethod
    @allure.step('Получить заказы конкретного пользователя')
    def get_user_orders(token: str) -> requests.Response:
        """
        Получает заказы авторизованного пользователя через GET /api/orders.
        Args:
            token (str): Строка авторизации в формате "Bearer <accessToken>".
        Return:
            requests.Response: HTTP-ответ библиотеки requests с кодом статуса и телом ответа.
        """
        return requests.get(
            f'{Config.MAIN_URL}{Config.URL_CREATE_ORDER}',
            headers={'Authorization': token}
        )