import pytest
import allure
from api.api_client import APIClient
from utils.methods import generate_random_string

@allure.epic("API Яндекс Самокат")
@allure.feature("Курьеры")
class TestCourier:

    def setup_method(self):
        self.api_client = APIClient()

    def make_payload(self, login=None, **overrides):
        payload = {
            "login": login or f"test_courier_{generate_random_string(8)}",
            "password": "test_pass_123",
            "firstName": "TestName",
        }
        payload.update(overrides)
        return payload

    def cleanup_courier(self, login, password):
        with allure.step(f"Очистка: удаление курьера '{login}'"):
            courier_id = self.api_client.get_courier_id(login, password)
            assert courier_id is not None, (
                f"Не удалось получить id курьера '{login}' для удаления — "
                f"курьер останется в базе"
            )
            delete_response = self.api_client.delete_courier(courier_id)
            assert delete_response.status_code == 200, (
                f"Не удалось удалить курьера '{login}' (id={courier_id}). "
                f"Статус: {delete_response.status_code}, Тело: {delete_response.text}"
            )

    @allure.story("Создание курьера с неполными данными")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    @allure.title("Ошибка 400 при отсутствии обязательного поля '{missing_field}'")
    def test_courier_creation_missing_required_field(self, missing_field):
        payload = self.make_payload()
        del payload[missing_field]

        response = self.api_client.create_courier(payload)

        with allure.step(f"Проверка статуса ответа при отсутствии поля '{missing_field}'"):
            assert response.status_code == 400, (
                f"Ожидался 400, получен {response.status_code}. Тело: {response.text}"
            )

        with allure.step("Проверка тела ошибки"):
            data = response.json()
            assert "message" in data, f"В теле ответа нет сообщения об ошибке: {data}"

    @allure.story("Создание курьера с неполными данными")
    @allure.title("Успешное создание курьера без поля 'firstName'")
    def test_courier_creation_without_first_name(self):
        payload = self.make_payload()
        del payload["firstName"]

        response = self.api_client.create_courier(payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 201, (
                f"Ожидался 201, получен {response.status_code}. Тело: {response.text}"
            )

        with allure.step("Проверка тела ответа"):
            data = response.json()
            assert data.get("ok") is True, f"Неверный формат ответа: {data}"

        self.cleanup_courier(payload["login"], payload["password"])

    @allure.story("Создание курьера")
    @allure.title("Попытка создания двух курьеров с одинаковым логином")
    def test_create_two_identical_couriers(self):
        payload = self.make_payload()

        first_response = self.api_client.create_courier(payload)
        with allure.step("Проверка создания первого курьера"):
            assert first_response.status_code == 201, (
                f"Первый курьер не создан: статус {first_response.status_code}, "
                f"тело: {first_response.text}"
            )

        second_response = self.api_client.create_courier(payload)
        with allure.step("Проверка статуса при повторном создании"):
            assert second_response.status_code == 409, (
                f"Ожидался 409 (логин уже используется), "
                f"получен {second_response.status_code}. Тело: {second_response.text}"
            )

        with allure.step("Проверка сообщения об ошибке"):
            data = second_response.json()
            assert "message" in data, f"В теле ответа нет сообщения об ошибке: {data}"

        self.cleanup_courier(payload["login"], payload["password"])

    @allure.story("Создание курьера")
    @allure.title("Попытка создания курьера с уже существующим логином (через фикстуру)")
    def test_create_courier_with_existing_login(self, new_courier):
        unique_login, _, _ = new_courier
        payload = self.make_payload(login=unique_login, password="new_password_456", firstName="NewUser")

        response = self.api_client.create_courier(payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 409, (
                f"Ожидался 409 (логин уже используется), "
                f"получен {response.status_code}. Тело: {response.text}"
            )

        with allure.step("Проверка сообщения об ошибке"):
            data = response.json()
            assert "message" in data, f"В теле ответа нет сообщения об ошибке: {data}"

