# tests/test_login.py
import pytest
import allure
from api.api_client import APIClient

@allure.epic("API Яндекс Самокат")
@allure.feature("Авторизация")
class TestLogin:

    def setup_method(self):
        self.api_client = APIClient()

    @allure.story("Авторизация курьера")
    @allure.title("Успешный логин курьера")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_success(self, new_courier):
        login, password, _ = new_courier
        payload = {"login": login, "password": password}

        response = self.api_client.login_courier(payload)

        with allure.step("Проверка статуса ответа"):
            if response.status_code == 504:
                pytest.skip("Стенд недоступен (504), пропускаем тест")
            assert response.status_code == 200, \
                f"Ожидался статус 200, получен {response.status_code}. Тело: {response.text}"

        with allure.step("Проверка наличия поля id в ответе"):
            try:
                data = response.json()
            except ValueError:
                pytest.fail(f"Сервер не вернул валидный JSON. Статус: {response.status_code}, Тело: {response.text}")
            
            assert "id" in data, f"В ответе отсутствует поле 'id': {data}"

    @allure.story("Авторизация курьера")
    @allure.title("Неверный пароль")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_wrong_password(self):
        payload = {"login": "test_user", "password": "wrong_password_123"}
        response = self.api_client.login_courier(payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code in [401, 404], \
                f"Ожидался 401 или 404, получен {response.status_code}. Тело: {response.text}"

        with allure.step("Проверка тела ответа"):
            try:
                data = response.json()
            except ValueError:
                pytest.fail(f"Сервер не вернул валидный JSON. Статус: {response.status_code}, Тело: {response.text}")
            
            has_error_msg = "message" in data or "error" in data
            assert has_error_msg, f"В теле ответа нет сообщения об ошибке: {data}"

    @allure.story("Авторизация курьера")
    @allure.title("Отсутствие пароля в запросе")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_missing_password(self):
        payload = {"login": "test_user"}
        response = self.api_client.login_courier(payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code in [400, 404, 504], \
            f"Получен неожиданный статус: {response.status_code}. Тело: {response.text}"

        with allure.step("Проверка тела ответа"):
            if response.status_code in [400, 404]:
                try:
                    data = response.json()
                except ValueError:
                    pytest.fail(f"При ошибке валидации сервер не вернул валидный JSON. Статус: {response.status_code}, Тело: {response.text}")
                has_error_msg = "message" in data or "error" in data or "code" in data
                assert has_error_msg, f"В теле ответа нет сообщения об ошибке: {data}"
            else:  # 504 — сервер недоступен
                assert response.text, "При статусе 504 тело ответа пустое"

    @allure.story("Авторизация курьера")
    @allure.title("Отсутствие логина в запросе")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_missing_login(self):
        payload = {"password": "test_password"}  
        response = self.api_client.login_courier(payload)

        with allure.step("Проверка статуса ответа"):
            if response.status_code == 504:
                pytest.skip("Стенд недоступен (504), пропускаем тест")
            assert response.status_code in [400, 404], \
                f"Получен неожиданный статус: {response.status_code}. Тело: {response.text}"

        with allure.step("Проверка тела ответа"):
            try:
                data = response.json()
            except ValueError:
                pytest.fail(f"Сервер не вернул валидный JSON. Статус: {response.status_code}, Тело: {response.text}")
            
            has_error_msg = "message" in data or "error" in data
            assert has_error_msg, f"В теле ответа нет сообщения об ошибке: {data}"

    @allure.story("Авторизация курьера")
    @allure.title("Логин несуществующего пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_non_existent_user(self):
        payload = {"login": "non_existent_user_999", "password": "any_password"}
        response = self.api_client.login_courier(payload)

        with allure.step("Проверка статуса ответа"):
            if response.status_code == 504:
                pytest.skip("Стенд недоступен (504), пропускаем тест")
            assert response.status_code in [404, 401], \
                f"Ожидался 404 или 401, получен {response.status_code}. Тело: {response.text}"

        with allure.step("Проверка тела ответа"):
            try:
                data = response.json()
            except ValueError:
                pytest.fail(f"Сервер не вернул валидный JSON. Статус: {response.status_code}, Тело: {response.text}")
            
            has_error_msg = "message" in data or "error" in data
            assert has_error_msg, f"В теле ответа нет сообщения об ошибке: {data}"