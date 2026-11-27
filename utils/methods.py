import string
import random
import logging
import pytest

import allure
from api.api_client import APIClient

logger = logging.getLogger("scooter_tests")


def generate_random_string(length: int) -> str:
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def register_new_courier_and_return_login_password() -> list:
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name,
    }

    allure.attach(
        str(payload),
        name="Данные для регистрации курьера",
        attachment_type=allure.attachment_type.TEXT
    )

    logger.info("Попытка регистрации курьера: логин=%s", login)

    api_client = APIClient()
    response = api_client.create_courier(payload)

    logger.info(
        "Регистрация курьера: логин=%s, статус=%s",
        login, response.status_code
    )

    if response.status_code != 201:
        logger.error(
            "Регистрация курьера '%s' не удалась: статус=%s, тело=%s",
            login, response.status_code, response.text
        )
        pytest.fail(
            f"Не удалось зарегистрировать курьера. "
            f"Статус: {response.status_code}, тело: {response.text}"
        )

    return [login, password, first_name]
