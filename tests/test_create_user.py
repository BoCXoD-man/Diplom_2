import allure

from base.user_base import UserBase
from data import TextResponse
import pytest
from http import HTTPStatus


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

    
    @allure.feature("Регистрация пользователя")
    @pytest.mark.parametrize(
        "missing_key, title",
        [
            ("email",    "Проверка ошибки 403 при регистрации с отсутствием почты"),
            ("password", "Проверка ошибки 403 при регистрации с отсутствием пароля"),
            ("name",     "Проверка ошибки 403 при регистрации с отсутствием имени"),
        ],
        ids=["no_email", "no_password", "no_name"]
    )
    def test_failed_registration_missing_field_code_403(self, new_user_body, missing_key, title):
        allure.dynamic.title(title)

        # Формируем тело без одного обязательного поля
        user_body = {k: v for k, v in new_user_body.items() if k != missing_key}

        with allure.step(f"Отправить запрос на регистрацию без поля '{missing_key}'"):
            response = UserBase.register_user(user_body)

        with allure.step("Проверить, что вернулся 403 и корректный текст ошибки"):
            assert response.status_code == HTTPStatus.FORBIDDEN, (
                f"Ожидался статус 403 при отсутствии '{missing_key}', "
                f"получено: {response.status_code}, body: {getattr(response, 'text', response)}"
            )
            assert response.text == TextResponse.INCORRECT_DATA_REG, (
                f"Ожидался текст '{TextResponse.INCORRECT_DATA_REG}', получено: {response.text}"
            )
