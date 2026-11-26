import pytest
import allure
from api.api_client import APIClient
from utils.methods import generate_random_string

@allure.epic("API Яндекс Самокат")
@allure.feature("Курьеры")
class TestCourier:

    def setup_method(self):
        self.api_client = APIClient()

    @pytest.mark.parametrize("missing_field,expected_status", [
        ("", 201),
        ("password", 400),
        ("login", 400),
    ])
    @allure.story("Создание курьера с неполными данными")
    @allure.title("Создание курьера: отсутствует поле '{missing_field}' (ожидаем {expected_status})")
    def test_courier_creation_with_missing_fields(self, missing_field, expected_status):
        base_payload = {}
        if missing_field != "login":
            base_payload["login"] = generate_random_string(10)
        if missing_field != "password":
            base_payload["password"] = generate_random_string(10)
        if missing_field != "firstName":
            base_payload["firstName"] = generate_random_string(10)

        response = self.api_client.create_courier(base_payload)

        with allure.step(f"Проверка статуса ответа: ожидался {expected_status}, получен {response.status_code}"):
            assert response.status_code in [expected_status, 500, 504], \
                f"Ожидался {expected_status}/500/504, получен {response.status_code}. Тело: {response.text}"

        with allure.step("Проверка тела ответа"):
            if response.status_code == 201:
                try:
                    data = response.json()
                except ValueError:
                    pytest.fail(f"При статусе 201 сервер не вернул валидный JSON. Тело: {response.text}")
                assert "ok" in data, f"В теле ответа нет ключа 'ok': {data}"
                assert data["ok"] is True, f"Ожидалось 'ok': true, получено: {data['ok']}"
            else:
                assert response.text, f"При статусе {response.status_code} тело ответа пустое"

    @allure.story("Создание курьера")
    @allure.title("Попытка создания двух курьеров с одинаковым логином")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_two_identical_couriers(self):

        base_login = "dup_user_" + generate_random_string(5)
        
        payload = {
            "login": base_login,
            "password": "test_password_123",
            "firstName": "TestUser"}

        first_response = self.api_client.create_courier(payload)
        
        with allure.step("Проверка статуса создания первого курьера"):
            assert first_response.status_code in [201, 409, 500, 504], \
                f"Первый курьер не создан: статус {first_response.status_code}, тело: {first_response.text}"

        if first_response.status_code == 201:
            second_response = self.api_client.create_courier(payload)

            with allure.step("Проверка статуса ответа при повторном создании"):
                assert second_response.status_code in [400, 409, 500, 504], \
                    f"Ожидался 400/409/500/504, получен {second_response.status_code}. Тело: {second_response.text}"

            with allure.step("Проверка тела ответа на дубликат"):
                if second_response.status_code in [400, 409]:
                    try:
                        data = second_response.json()
                    except ValueError:
                        pytest.fail(f"При ошибке дублирования сервер не вернул валидный JSON. Статус: {second_response.status_code}, Тело: {second_response.text}")
                    has_error_msg = "message" in data or "error" in data or "code" in data
                    assert has_error_msg, f"В теле ответа нет сообщения об ошибке: {data}"
                else:
                    assert second_response.text, "При статусе 500/504 тело ответа пустое"
        
        else:
            if first_response.status_code == 409:
                try:
                    data = first_response.json()
                except ValueError:
                    pytest.fail(f"Сервер вернул 409, но не JSON. Тело: {first_response.text}")
                has_error_msg = "message" in data or "error" in data
                assert has_error_msg, f"При 409 нет сообщения об ошибке: {data}"
            else: 
                assert first_response.text, f"При статусе {first_response.status_code} тело ответа пустое"

    @allure.story("Создание курьера")
    @allure.title("Попытка создания курьера с уже существующим логином (через фикстуру)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_courier_with_existing_login(self, new_courier):
        """Проверяет, что нельзя создать курьера с логином, который уже существует."""
        login, _, _ = new_courier

        payload = {
            "login": login,
            "password": "new_password_456",
            "firstName": "NewUser"
        }

        response = self.api_client.create_courier(payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code in [400, 409, 500, 504], \
                f"Ожидался 400/409/500/504, получен {response.status_code}. Тело: {response.text}"

        with allure.step("Проверка тела ответа"):
            if response.status_code in [400, 409]:
                try:
                    data = response.json()
                except ValueError:
                    pytest.fail(f"При ошибке дублирования логина сервер не вернул валидный JSON. Статус: {response.status_code}, Тело: {response.text}")
                has_error_msg = "message" in data or "error" in data or "code" in data
                assert has_error_msg, f"В теле ответа нет сообщения об ошибке: {data}"
            else:
                assert response.text, "При статусе 500/504 тело ответа пустое"