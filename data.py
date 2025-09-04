class Config:
    """Конфигурационный класс для API запросов."""
    MAIN_URL: str = 'https://stellarburgers.nomoreparties.site'
    URL_REGISTRATION: str = '/api/auth/register'
    URL_LOGIN: str = '/api/auth/login'
    URL_LOGOUT: str = '/api/auth/logout'
    URL_CREATE_TOKEN: str = '/api/auth/token'
    URL_CHANGE_USER_DATA: str = '/api/auth/user'
    URL_DELETE_USER: str = '/api/auth/user'
    URL_CREATE_ORDER: str = '/api/orders'
    URL_GET_USER_ORDERS: str = '/api/orders'


class TextResponse:
    """Тексты ожидаемых сообщений об ошибках/успехе для проверок API."""
    ALREADY_EXIST_USER_REG: str = '{"success":false,"message":"User already exists"}'
    INCORRECT_DATA_REG: str = '{"success":false,"message":"Email, password and name are required fields"}'
    INCORRECT_DATA_LOGIN: str = '{"success":false,"message":"email or password are incorrect"}'
    UNAUTHORIZED_USER: str = '{"success":false,"message":"You should be authorised"}'
    INCORRECT_EMAIL_UPDATE: str = '{"success":false,"message":"User with such email already exists"}'
    NO_INGREDIENTS: str = '{"success":false,"message":"Ingredient ids must be provided"}'


class IngredientsData:
    """Наборы данных для тела заказа с корректными и некорректными ингредиентами."""

    INGREDIENTS_BODY: dict[str, list[str]] = {
        'ingredients': [
            '61c0c5a71d1f82001bdaaa6d',
            '61c0c5a71d1f82001bdaaa6f',
            '61c0c5a71d1f82001bdaaa72',
        ]
    }
    INVALID_INGREDIENTS_BODY: dict[str, list[str]] = {
        'ingredients': ['66666666666hhhhhhhhhhhh']
    }