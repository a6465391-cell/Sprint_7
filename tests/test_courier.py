import requests
import allure
from config.config import BASE_URL
from utils.methods import generate_random_string

@allure.epic("API Яндекс Самокат")
@allure.feature("Курьеры")
class TestCourier:

    @allure.story("Создание курьера")
    @allure.title("Успешное создание курьера")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_courier_success(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post(f"{BASE_URL}/api/v1/courier", json=payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 201, f"Ожидался 201, получен {response.status_code}"

        with allure.step("Проверка тела ответа"):
            assert response.json() == {"ok": True}, f"Ожидался {{'ok': True}}, получен {response.text}"

    @allure.story("Создание курьера")
    @allure.title("Дублирование курьера")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_courier_duplicate(self):
        login = generate_random_string(10)
        
        # 1. Создаем первого
        payload_first = {
            "login": login,
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        resp_first = requests.post(f"{BASE_URL}/api/v1/courier", json=payload_first)
        with allure.step("Проверка успешной регистрации первого курьера"):
            assert resp_first.status_code == 201, f"Не удалось зарегистрировать первого курьера: {resp_first.text}" 
        
        # 2. Пробуем создать второго с тем же логином
        payload_second = {
            "login": login,
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        response = requests.post(f"{BASE_URL}/api/v1/courier", json=payload_second)
        
        with allure.step(f"Статус ответа при дубликате: {response.status_code}"):
            # ИСПРАВЛЕНО: теперь ожидаем 409
            assert response.status_code == 409, f"Ожидался 409, получен {response.status_code}"
        
        with allure.step("Проверка сообщения об ошибке"):
            resp_text = response.text.lower()
            assert "уже используется" in resp_text, \
                f"Не найдено сообщение об ошибке дубликата: {response.text}"
    @allure.story("Создание курьера")
    @allure.title("Отсутствие обязательного поля")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_courier_missing_field(self):
        payload = {
            "login": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        response = requests.post(f"{BASE_URL}/api/v1/courier", json=payload)
        
        with allure.step(f"Статус ответа при отсутствии поля: {response.status_code}"):
            assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"