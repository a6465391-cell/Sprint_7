import time
import allure
from api.api_client import APIClient

@allure.epic("API Яндекс Самокат")
@allure.feature("Заказы")
class TestGetOrders:

    def setup_method(self):
        self.api_client = APIClient()

    def make_order_payload(self, **overrides):
        payload = {
            "firstName": "Тест",
            "lastName": "Тестов",
            "address": "ул. Ленина, 1",
            "metroStation": 4,
            "phone": "+7 999 000 00 00",
            "rentTime": 5,
            "deliveryDate": "2026-12-01",
            "comment": "Тест заказа для проверки списка",
        }
        payload.update(overrides)
        return payload

    @allure.story("Получение списка заказов")
    @allure.title("Успешное получение списка заказов (структура ответа)")
    def test_get_orders_list_success(self):
        response = self.api_client.get_orders()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, \
                f"Ожидался статус 200, получен {response.status_code}. Тело: {response.text}"

        with allure.step("Проверка структуры ответа"):
            data = response.json()
            assert "orders" in data, f"В ответе нет ключа 'orders': {data}"
            assert isinstance(data["orders"], list), \
                f"'orders' не является списком: {type(data['orders'])}"

    @allure.story("Получение списка заказов")
    @allure.title("Заказ появляется в списке после создания")
    def test_get_orders_after_creation(self):
        create_response = self.api_client.create_order(self.make_order_payload())

        with allure.step("Проверка статуса создания заказа"):
            assert create_response.status_code == 201, \
                f"Ожидался статус 201, получен {create_response.status_code}. Тело: {create_response.text}"

        with allure.step("Получение track созданного заказа"):
            created_order_track = create_response.json().get("track")
            assert created_order_track, \
                f"Не удалось получить track из ответа: {create_response.json()}"

        with allure.step("Ожидание появления заказа в списке"):
            time.sleep(1)

        get_response = self.api_client.get_orders()

        with allure.step("Проверка статуса получения списка"):
            assert get_response.status_code == 200, \
                f"Ожидался статус 200, получен {get_response.status_code}. Тело: {get_response.text}"

        with allure.step("Проверка наличия заказа в списке"):
            data = get_response.json()
            assert "orders" in data, f"В ответе нет ключа 'orders': {data}"
            assert isinstance(data["orders"], list), \
                f"'orders' не является списком: {type(data['orders'])}"

            found = any(order.get("track") == created_order_track for order in data["orders"])
            assert found, \
                f"Заказ с track={created_order_track} не найден в списке. Список: {data['orders']}"
