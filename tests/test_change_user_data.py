import allure
from data import TextResponse
from base.user_base import UserBase


class TestUpdateUserData:
    """
    Тесты обновления данных пользователя /api/auth/user.
    """

    @allure.title('Проверка успешного изменения почты, код 200')
    def test_successful_update_email_code_200(self, new_user):
        """
        Args:
            new_user (dict): данные пользователя и токены: {"user_body": dict, "token": str, "refresh_token": str}
        """
        user = new_user
        body = {"email": f"addtest{user['user_body']['email']}"}
        response = UserBase.update_user(user["token"], body)
        assert response.status_code == 200 and response.json()["user"]["email"] == body["email"]

    @allure.title('Проверка успешного изменения имени, код 200')
    def test_successful_update_name_code_200(self, new_user):
        """
        Args:
            new_user (dict): данные пользователя и токены: {"user_body": dict, "token": str, "refresh_token": str}
        """
        user = new_user
        body = {"name": f"addtest{user['user_body']['name']}"}
        response = UserBase.update_user(user["token"], body)
        assert response.status_code == 200 and response.json()["user"]["name"] == body["name"]

    @allure.title('Проверка ошибки 401 при изменении данных без авторизации')
    def test_failed_update_unauthorized_code_401(self):
        """Тело запроса пустое, заголовок Authorization не передаём (передаётся пустая строка)."""
        response = UserBase.update_user(token="", body={})
        assert response.status_code == 401 and response.text == TextResponse.UNAUTHORIZED_USER

    @allure.title('Проверка ошибки 403 при изменении на уже существующую почту')
    def test_failed_update_email_already_exist_code_403(self, new_user, new_user_2):
        """
        Args:
            new_user (dict): первый пользователь (изменяем его email)
            new_user_2 (dict): второй пользователь (берём его email как уже существующий)
        """
        user_1 = new_user
        user_2 = new_user_2
        body = {"email": user_2["user_body"]["email"]}
        response = UserBase.update_user(user_1["token"], body)
        assert response.status_code == 403 and response.text == TextResponse.INCORRECT_EMAIL_UPDATE