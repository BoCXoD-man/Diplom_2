import allure
import pytest

from helpers import generate_user_data
from base.user_base import UserBase


@pytest.fixture
def new_user_body() -> dict:
    """
    Генерирует валидное тело для регистрации пользователя.
    Return:
        dict: {"email": str, "password": str, "name": str}
    """
    with allure.step("Сгенерировать данные нового пользователя"):
        email, password, name = generate_user_data()
        return {"email": email, "password": password, "name": name}


@pytest.fixture
def new_user():
    """
    Создаёт пользователя через API и возвращает его данные и токены; после теста удаляет пользователя.
    Return:
        dict: {"user_body": dict, "token": str, "refresh_token": str}
    """
    with allure.step("Создать нового пользователя"):
        email, password, name = generate_user_data()
        user_body = {"email": email, "password": password, "name": name}

        response = UserBase.register_user(user_body)
        # Диагностика в отчёте на случай падения
        allure.attach(str(response.status_code), "status_code", allure.attachment_type.TEXT)
        try:
            allure.attach(response.text, "response_body", allure.attachment_type.JSON)
        except Exception:
            allure.attach(response.text, "response_body", allure.attachment_type.TEXT)

        assert response.status_code == 200, "Регистрация пользователя не удалась"
        resp_json = response.json()
        token = resp_json["accessToken"]
        refresh_token = resp_json["refreshToken"]

        user_data = {"user_body": user_body, "token": token, "refresh_token": refresh_token}
        yield user_data

    with allure.step("Удалить пользователя (teardown)"):
        # если токен вдруг пустой/битый — пусть падение будет видно в отчёте
        del_resp = UserBase.delete_user(token)
        allure.attach(str(del_resp.status_code), "delete_status", allure.attachment_type.TEXT)
        # Не делаем assert здесь, чтобы не скрывать основной фейл теста


@pytest.fixture
def new_user_2():
    """
    Создаёт дополнительного пользователя через API и возвращает его данные и токены; после теста удаляет пользователя.
    Return:
        dict: {"user_body": dict, "token": str, "refresh_token": str}
    """
    with allure.step("Создать дополнительного нового пользователя"):
        email, password, name = generate_user_data()
        user_body = {"email": email, "password": password, "name": name}

        response = UserBase.register_user(user_body)
        allure.attach(str(response.status_code), "status_code", allure.attachment_type.TEXT)
        try:
            allure.attach(response.text, "response_body", allure.attachment_type.JSON)
        except Exception:
            allure.attach(response.text, "response_body", allure.attachment_type.TEXT)

        assert response.status_code == 200, "Регистрация дополнительного пользователя не удалась"
        resp_json = response.json()
        token = resp_json["accessToken"]
        refresh_token = resp_json["refreshToken"]

        user_data = {"user_body": user_body, "token": token, "refresh_token": refresh_token}
        yield user_data

    with allure.step("Удалить дополнительного пользователя (teardown)"):
        del_resp = UserBase.delete_user(token)
        allure.attach(str(del_resp.status_code), "delete_status", allure.attachment_type.TEXT)


@pytest.fixture
def new_user_cleanup(new_user_body: dict):
    """
    Возвращает сгенерированное тело пользователя; после теста логинится и удаляет его.
    Return:
        dict: {"email": str, "password": str, "name": str}
    """
    with allure.step("Создать данные для пользователя"):
        user_body = new_user_body
        yield user_body

    with allure.step("Логин и удаление пользователя по данным фикстуры (teardown)"):
        login_resp = UserBase.login_user({"email": user_body["email"], "password": user_body["password"]})
        allure.attach(str(login_resp.status_code), "login_status", allure.attachment_type.TEXT)
        try:
            allure.attach(login_resp.text, "login_response", allure.attachment_type.JSON)
        except Exception:
            allure.attach(login_resp.text, "login_response", allure.attachment_type.TEXT)

        assert login_resp.status_code == 200, "Логин для удаления пользователя не удался"
        token = login_resp.json()["accessToken"]

        del_resp = UserBase.delete_user(token)
        allure.attach(str(del_resp.status_code), "delete_status", allure.attachment_type.TEXT)