import sys
import os

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import allure
import pytest
from api.api_client import APIClient
from utils.methods import register_new_courier_and_return_login_password

@pytest.fixture
def new_courier():
    api_client = APIClient()

    login, password, first_name = register_new_courier_and_return_login_password()

    allure.attach(
        f"Создан курьер: login={login}, first_name={first_name}",
        name="Создание тестового курьера",
        attachment_type=allure.attachment_type.TEXT
    )

    if not login:
        pytest.fail("Не удалось создать тестового курьера для запуска теста")
    try:
        yield login, password, first_name        
    finally:

        try:

            response = api_client.delete_courier(login)

            if response.status_code == 200:
                allure.attach(
                    f"Курьер {login} успешно удален.",
                    name="Очистка данных",
                    attachment_type=allure.attachment_type.TEXT)
            elif response.status_code == 404:
                allure.attach(
                    f"Курьер {login} уже был удален ранее или не найден (404).",
                    name="Очистка данных",
                    attachment_type=allure.attachment_type.TEXT)
            else:
                allure.attach(
                    f"Попытка удаления курьера {login} вернула статус {response.status_code}. Тело: {response.text}",
                    name="Ошибка очистки",
                    attachment_type=allure.attachment_type.TEXT)
                
        except Exception as e:
            allure.attach(
                f"Критическая ошибка при удалении курьера: {str(e)}",
                name="Ошибка очистки",
                attachment_type=allure.attachment_type.TEXT)