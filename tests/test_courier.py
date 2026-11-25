import pytest
import allure
from api.api_client import APIClient
from utils.methods import generate_random_string

@allure.epic("API Яндекс Самокат")
@allure.feature("Курьеры")
class TestCourier:

    def setup_method(self):
        self.api_client = APIClient()

    @pytest.mark.parametrize("missing_field,expected_status,expected_body_key", [
        ("", 201, "ok"),           
        ("password", 400, "message"),  
        ("login", 400, "message"), ])
    
    @allure.story("Создание курьера с неполными данными")
    def test_courier_creation_with_missing_fields(self, missing_field, expected_status, expected_body_key):

        base_payload = {}
        if missing_field != "login":
            base_payload["login"] = generate_random_string(10)
        if missing_field != "password":
            base_payload["password"] = generate_random_string(10)
        if missing_field != "firstName":
            base_payload["firstName"] = generate_random_string(10)

        try:
            response = self.api_client.register_courier(base_payload)
        except Exception as e:
            pytest.fail(f"Запрос на регистрацию курьера упал: {e}")

        with allure.step(f"Проверка статуса ответа: ожидался {expected_status}, получен {response.status_code}"):
            assert response.status_code == expected_status

        with allure.step("Проверка тела ответа"):
            data = response.json()
            if expected_status == 201:                
                assert expected_body_key in data, f"В теле ответа нет ключа {expected_body_key}: {data}"
                assert data[expected_body_key] is True, f"Ожидалось {expected_body_key}: true, получено: {data[expected_body_key]}"
            else:            
                error_keys = [key for key in data.keys() if key in ["message", "error"]]
                assert len(error_keys) > 0, f"В теле ответа нет сообщения об ошибке: {data}"

                error_message = data[error_keys[0]]
                assert error_message, f"Сообщение об ошибке пустое: {data}"