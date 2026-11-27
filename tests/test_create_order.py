import pytest
import allure
from api.api_client import APIClient

@allure.epic("API Яндекс Самокат")
@allure.feature("Заказы")
class TestCreateOrder:

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
            "comment": "Тест заказа",
        }
        payload.update(overrides)
        return payload

    def cancel_order_if_created(self, response):
        with allure.step("Очистка: отмена заказа"):
            if response.status_code == 201:
                track = response.json().get("track")
                assert track is not None, f"Не найден track заказа для отмены: {response.json()}"
                cancel_response = self.api_client.cancel_order(track)
                assert cancel_response.status_code == 200, (
                    f"Не удалось отменить заказ (track={track}). "
                    f"Статус: {cancel_response.status_code}, Тело: {cancel_response.text}"
                )

    @allure.story("Создание заказа с разными цветами")
    @allure.title("Заказ создаётся: {title}")
    @pytest.mark.parametrize("color,title", [
        (None, "без цвета"),
        (["BLACK"], "цвет BLACK"),
        (["GREY"], "цвет GREY"),
        (["BLACK", "GREY"], "оба цвета"),
    ])
    def test_create_order_with_colors(self, color, title):
        payload = self.make_order_payload()
        if color is not None:
            payload["color"] = color

        response = self.api_client.create_order(payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 201, (
                f"Ожидался 201, получен {response.status_code}. Тело: {response.text}"
            )

        with allure.step("Проверка тела ответа"):
            data = response.json()
            assert "track" in data, f"При успехе (201) не найдено поле 'track': {data}"

        self.cancel_order_if_created(response)

