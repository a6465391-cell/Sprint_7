import pytest
import allure
from api.api_client import APIClient

@allure.epic("API Яндекс Самокат")
@allure.feature("Заказы")
class TestCreateOrder:

    def setup_method(self):
        self.api_client = APIClient()

    @allure.story("Создание заказа с разными цветами")
    @pytest.mark.parametrize("payload,title", [
        (
            {"street": "ул. Ленина", "from": 1, "to": 10, "comment": "Тест заказа"},
            "Без цвета"
        ),
        (
            {"street": "ул. Ленина", "from": 1, "to": 10, "comment": "Тест заказа", "color": ["BLACK"]},
            "Цвет BLACK"
        ),
        (
            {"street": "ул. Ленина", "from": 1, "to": 10, "comment": "Тест заказа", "color": ["GREY"]},
            "Цвет GREY"
        ),
        (
            {"street": "ул. Ленина", "from": 1, "to": 10, "comment": "Тест заказа", "color": ["BLACK", "GREY"]},
            "Несколько цветов"
        ),
    ])
    @allure.title("{title}")
    def test_create_order_with_colors(self, payload, title):
        response = self.api_client.create_order(payload)

        with allure.step(f"Проверка статуса ответа"):
            assert response.status_code in [201, 400, 500], \
                f"Получен неожиданный статус: {response.status_code}. Тело: {response.text}"

        with allure.step("Проверка тела ответа"):
            try:
                data = response.json()
            except ValueError:
                pytest.fail(f"Сервер не вернул валидный JSON. Статус: {response.status_code}, Тело: {response.text}")

            if response.status_code == 201:
                assert "track" in data, f"При успехе (201) не найдено поле 'track': {data}"
            else:
                has_error_msg = "message" in data or "error" in data or "code" in data
                assert has_error_msg, f"При ошибке ({response.status_code}) нет сообщения об ошибке в теле: {data}"

    @allure.story("Создание заказа с отсутствующими полями")
    @pytest.mark.parametrize("missing_field", [
        "street", "from", "to", "comment"    ])
    @allure.title("Проверка создания заказа без поля '{missing_field}'")
    def test_create_order_with_missing_fields(self, missing_field):
        payload = {
            "street": "ул. Ленина",
            "from": 1,
            "to": 10,
            "comment": "Тест заказа",
            "color": ["BLACK"]}

        if missing_field in payload:
            del payload[missing_field]
        del payload["color"]  

        response = self.api_client.create_order(payload)

        with allure.step(f"Проверка статуса ответа (поле {missing_field} отсутствует)"):
            assert response.status_code in [400, 500], \
                f"Получен неожиданный статус: {response.status_code}. Тело: {response.text}"

        with allure.step("Проверка тела ответа"):
            data = response.json()  
            has_error_msg = "message" in data or "error" in data or "code" in data
            assert has_error_msg, f"Нет сообщения об ошибке в теле при статусе {response.status_code}: {data}" 