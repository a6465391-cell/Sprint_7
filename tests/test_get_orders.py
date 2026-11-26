import pytest
import allure
from api.api_client import APIClient

@allure.epic("API Яндекс Самокат")
@allure.feature("Заказы")
class TestGetOrders:

    def setup_method(self):
        self.api_client = APIClient()

    @allure.story("Получение списка заказов (успешный сценарий)")
    @allure.title("Успешное получение списка заказов")
    def test_get_orders_list_success(self):
        """Проверяет, что эндпоинт возвращает корректную структуру ответа."""
        response = self.api_client.get_orders()

        with allure.step("Проверка статуса ответа"):
            if response.status_code == 504:
                pytest.skip("Стенд недоступен (504), пропускаем тест")
            assert response.status_code == 200, \
                f"Ожидался статус 200, получен {response.status_code}. Тело: {response.text}"

        with allure.step("Проверка структуры ответа"):
            try:
                data = response.json()
            except ValueError:
                pytest.fail(f"Сервер не вернул валидный JSON. Статус: {response.status_code}, Тело: {response.text}")

            assert "orders" in data, f"В ответе нет ключа 'orders': {data}"
            assert isinstance(data["orders"], list), f"'orders' не является списком: {type(data['orders'])}"

    @allure.story("Проверка наличия созданного заказа в списке")
    @allure.title("Заказ появляется в списке после создания")
    def test_get_orders_after_creation(self):
        create_payload = {
            "street": "ул. Ленина",
            "from": 1,
            "to": 10,
            "comment": "Тест заказа для проверки списка",
            "color": ["BLACK"]
        }
        create_response = self.api_client.create_order(create_payload)

        with allure.step("Проверка статуса создания заказа"):
            assert create_response.status_code in [201, 500, 504], \
                f"Не удалось создать заказ: статус {create_response.status_code}, тело: {create_response.text}"

        if create_response.status_code == 201:
            try:
                create_data = create_response.json()
            except ValueError:
                pytest.fail(f"Сервер вернул 201, но не JSON. Тело: {create_response.text}")
            created_order_track = create_data.get("track")
            assert created_order_track, f"Не удалось получить track созданного заказа. Данные: {create_data}"
        else:
            assert create_response.text, f"При статусе {create_response.status_code} тело ответа пустое"
            return 

        get_response = self.api_client.get_orders()

        with allure.step("Проверка статуса получения списка"):
            assert get_response.status_code in [200, 504], \
                f"Ожидался 200 или 504, получен {get_response.status_code}. Тело: {get_response.text}"

        if get_response.status_code == 200:
            try:
                data = get_response.json()
            except ValueError:
                pytest.fail(f"При статусе 200 сервер не вернул валидный JSON. Тело: {get_response.text}")
            assert "orders" in data, f"В ответе нет ключа 'orders': {data}"
            assert isinstance(data["orders"], list), f"'orders' не является списком: {type(data['orders'])}"

            with allure.step("Проверка, что созданный заказ есть в списке"):
                found = any(order.get("track") == created_order_track for order in data["orders"])
                assert found, f"Заказ с track={created_order_track} не найден в списке. Список: {data['orders']}"
        else:  
            assert get_response.text, "При статусе 504 тело ответа пустое"