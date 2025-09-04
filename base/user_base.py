import allure
import requests

from data import Config


class UserBase:
    """
    Базовые методы работы с аутентификацией и профилем пользователя в Stellar Burgers.
    """

    @staticmethod
    @allure.step('Зарегистрировать пользователя')
    def register_user(body: dict) -> requests.Response:
        """
        Регистрирует нового пользователя через POST /api/auth/register.
        Args:
            body (dict): Тело запроса в формате JSON: {"email": str, "password": str, "name": str}.
        Return:
            requests.Response: HTTP-ответ библиотеки requests с кодом статуса и телом ответа.
        """
        return requests.post(
            f'{Config.MAIN_URL}{Config.URL_REGISTRATION}',
            json=body
        )

    @staticmethod
    @allure.step('Авторизоваться в сервисе')
    def login_user(body: dict) -> requests.Response:
        """
        Выполняет вход пользователя через POST /api/auth/login.
        Args:
            body (dict): Тело запроса в формате JSON: {"email": str, "password": str}.
        Return:
            requests.Response: HTTP-ответ библиотеки requests с кодом статуса и телом ответа.
        """
        return requests.post(
            f'{Config.MAIN_URL}{Config.URL_LOGIN}',
            json=body
        )

    @staticmethod
    @allure.step('Обновить данные пользователя')
    def update_user(token: str, body: dict) -> requests.Response:
        """
        Обновляет данные профиля через PATCH /api/auth/user.
        Args:
            token (str): Строка авторизации в формате "Bearer <accessToken>".
            body (dict): Тело запроса в формате JSON. Допустимые поля: "email", "name", "password".
        Return:
            requests.Response: HTTP-ответ библиотеки requests с кодом статуса и телом ответа.
        """
        return requests.patch(
            f'{Config.MAIN_URL}{Config.URL_CHANGE_USER_DATA}',
            headers={'Authorization': token},
            json=body
        )

    @staticmethod
    @allure.step('Выйти из системы')
    def logout_user(body: dict) -> requests.Response:
        """
        Выполняет выход через POST /api/auth/logout.
        Args:
            body (dict): Тело запроса в формате JSON: {"token": str} — refresh-токен.
        Return:
            requests.Response: HTTP-ответ библиотеки requests с кодом статуса и телом ответа.
        """
        return requests.post(
            f'{Config.MAIN_URL}{Config.URL_LOGOUT}',
            json=body
        )

    @staticmethod
    @allure.step('Удалить пользователя')
    def delete_user(token: str) -> requests.Response:
        """
        Удаляет текущего пользователя через DELETE /api/auth/user.
        Args:
            token (str): Строка авторизации в формате "Bearer <accessToken>".
        Return:
            requests.Response: HTTP-ответ библиотеки requests с кодом статуса и телом ответа.
        """
        return requests.delete(
            f'{Config.MAIN_URL}{Config.URL_DELETE_USER}',
            headers={'Authorization': token}
        )