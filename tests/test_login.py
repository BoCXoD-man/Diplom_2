import allure
import pytest

from base.user_base import UserBase
from data import TextResponse


class TestLogin:
    """Тесты авторизации пользователя /api/auth/login."""

    @allure.title('Проверка успешной авторизации, код 200')
    def test_successful_login_code_200(self, new_user):
        """
        Args:
            new_user (dict): данные пользователя и токены: {"user_body": dict, "token": str, "refresh_token": str}
        """
        user = new_user
        body = {
            "email": user["user_body"]["email"],
            "password": user["user_body"]["password"],
        }
        response = UserBase.login_user(body)
        assert response.status_code == 200 and response.json()["user"]["email"] == body["email"]

    @allure.title('Проверка ошибки 401 при авторизации с неверными логином или паролем')
    @pytest.mark.parametrize(
        "email,password",
        [
            (lambda user: f'test{user["user_body"]["email"]}', lambda user: user["user_body"]["password"]),
            (lambda user: user["user_body"]["email"], lambda user: f'test{user["user_body"]["password"]}'),
        ],
        ids=["wrong_email", "wrong_password"],
    )
    def test_failed_login_wrong_credentials_code_401(self, new_user, email, password):
        """
        Args:
            new_user (dict): данные пользователя и токены
            email (callable): функция, возвращающая email на базе данных фикстуры
            password (callable): функция, возвращающая пароль на базе данных фикстуры
        """
        user = new_user
        body = {
            "email": email(user),
            "password": password(user),
        }
        response = UserBase.login_user(body)
        assert response.status_code == 401 and response.text == TextResponse.INCORRECT_DATA_LOGIN
