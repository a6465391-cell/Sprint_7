import sys
import os

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import pytest
import allure
from api.api_client import APIClient
from utils.methods import generate_random_string


@pytest.fixture
def new_courier():
    api_client = APIClient()

    login = f"test_courier_{generate_random_string(8)}"
    password = "test_pass_123"
    first_name = "TestName"

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = api_client.create_courier(payload)

    if response.status_code != 201:
        pytest.fail(
            f"Не удалось создать курьера для теста. "
            f"Статус: {response.status_code}, Тело: {response.text}"
        )

    yield login, password, first_name

    with allure.step(f"Очистка: удаление курьера '{login}'"):
        courier_id = api_client.get_courier_id(login, password)
        assert courier_id is not None, (
            f"Не удалось получить id курьера '{login}' для удаления — "
            f"курьер останется в базе"
        )

        delete_response = api_client.delete_courier(courier_id)
        if delete_response.status_code != 200:
            pytest.fail(
                f"Не удалось удалить курьера '{login}' (id={courier_id}). "
                f"Статус: {delete_response.status_code}, Тело: {delete_response.text}"
            )
