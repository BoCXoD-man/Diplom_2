import allure

from base.user_base import UserBase
from data import TextResponse


class TestRegistration:
    """Тесты регистрации пользователя /api/auth/register."""

    @allure.title('Проверка успешной регистрации пользователя, код 200')
    def test_successful_registration_code_200(self, new_user_cleanup):
        """
        Args:
            new_user_cleanup (dict): тело пользователя {"email": str, "password": str, "name": str}
        """
        user_body = new_user_cleanup
        response = UserBase.register_user(user_body)
        assert response.status_code == 200 and response.json()['user']['email'] == user_body['email']

    @allure.title('Проверка ошибки 403 при регистрации пользователя с уже существующими данными')
    def test_failed_registration_duplicate_user_code_403(self, new_user):
        """
        Args:
            new_user (dict): уже созданный пользователь {"user_body": dict, "token": str, "refresh_token": str}
        """
        response = UserBase.register_user(new_user['user_body'])
        assert response.status_code == 403 and response.text == TextResponse.ALREADY_EXIST_USER_REG

    @allure.title('Проверка ошибки 403 при регистрации с отсутствием почты')
    def test_failed_registration_no_email_code_403(self, new_user_body):
        """
        Args:
            new_user_body (dict): валидное тело пользователя для модификации
        """
        user_body = {'password': new_user_body['password'], 'name': new_user_body['name']}
        response = UserBase.register_user(user_body)
        assert response.status_code == 403 and response.text == TextResponse.INCORRECT_DATA_REG

    @allure.title('Проверка ошибки 403 при регистрации с отсутствием пароля')
    def test_failed_registration_no_password_code_403(self, new_user_body):
        """
        Args:
            new_user_body (dict): валидное тело пользователя для модификации
        """
        user_body = {'email': new_user_body['email'], 'name': new_user_body['name']}
        response = UserBase.register_user(user_body)
        assert response.status_code == 403 and response.text == TextResponse.INCORRECT_DATA_REG

    @allure.title('Проверка ошибки 403 при регистрации с отсутствием имени')
    def test_failed_registration_no_name_code_403(self, new_user_body):
        """
        Args:
            new_user_body (dict): валидное тело пользователя для модификации
        """
        user_body = {'email': new_user_body['email'], 'password': new_user_body['password']}
        response = UserBase.register_user(user_body)
        assert response.status_code == 403 and response.text == TextResponse.INCORRECT_DATA_REG
