import requests
from config.config import BASE_URL
import allure

class APIClient:
    def __init__(self):
        self.base_url = BASE_URL

    @allure.step("Регистрация нового курьера")
    def register_courier(self, payload):
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/courier",
                json=payload,
                timeout=60
            )
            return response
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Не удалось отправить запрос на регистрацию курьера: {e}")

    @allure.step("Авторизация курьера")
    def login_courier(self, payload):
        """Отправляет POST запрос на авторизацию курьера."""
        try:
            
            response = requests.post(
                f"{self.base_url}/api/v1/courier/login", 
                json=payload, 
                timeout=60
            )
            return response
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Не удалось отправить запрос на авторизацию: {e}")

    @allure.step("Создание заказа")
    def create_order(self, payload):
        """Отправляет POST запрос на создание заказа."""
        try:
            
            response = requests.post(
                f"{self.base_url}/api/v1/orders", 
                json=payload, 
                timeout=60
            )
            return response
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Не удалось отправить запрос на создание заказа: {e}")

    @allure.step("Получение списка заказов")
    def get_orders(self):
        """Отправляет GET запрос на получение списка заказов."""
        try:
            
            response = requests.get(
                f"{self.base_url}/api/v1/orders", 
                timeout=60
            )
            return response
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Не удалось получить список заказов: {e}")