import pytest
import allure
import requests
from config.config import BASE_URL

@allure.epic("API Яндекс Самокат")
@allure.feature("Заказы")
class TestOrders:

    # ИСПРАВЛЕНО: цвета передаются как списки, а не строки
    @allure.story("Создание заказа")
    @pytest.mark.parametrize("color", [None, ["BLACK"], ["GREY"], ["BLACK", "GREY"]])
    @allure.title("Создание заказа с цветом: {color}")
    def test_create_order_with_colors(self, color):
        payload = {
            "street": "ул. Ленина",
            "from": 1,
            "to": 10,
            "comment": "Тест заказа"
        }
        
        # Если цвет задан, передаем его как есть (это уже список)
        if color is not None:
            payload["color"] = color

        response = requests.post(f"{BASE_URL}/api/v1/orders", json=payload)
        
        with allure.step(f"Статус ответа: {response.status_code}"):
            assert response.status_code == 201, f"Ожидался 201, получен {response.status_code}. Тело: {response.text}"
        
        with allure.step("Проверка наличия поля track"):
            data = response.json()
            assert "track" in data, f"В ответе отсутствует поле track: {data}"

    @allure.story("Список заказов")
    @allure.title("Получение списка заказов")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_orders_list(self):
        response = requests.get(f"{BASE_URL}/api/v1/orders")
        
        with allure.step(f"Статус ответа: {response.status_code}"):
            assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
        
        with allure.step("Проверка структуры ответа"):
            data = response.json()
            # ИСПРАВЛЕНО: API возвращает словарь с ключом 'orders', внутри которого список
            assert "orders" in data, f"В ответе отсутствует ключ 'orders': {data}"
            assert isinstance(data["orders"], list), f"Поле 'orders' не является списком: {type(data['orders'])}"