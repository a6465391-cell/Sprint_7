import requests

class APIClient:
    def __init__(self, base_url="https://qa-scooter.praktikum-services.ru/api/v1"):
        self.base_url = base_url
        self.session = requests.Session()

    def create_courier(self, payload):
        """Создаёт курьера через POST /courier"""
        url = f"{self.base_url}/courier"
        response = self.session.post(url, data=payload)
        return response

    # 👇 ЭТОГО МЕТОДА НЕ ХВАТАЛО 👇
    def register_courier(self, payload):
        """Алиас для create_courier — нужен для совместимости с conftest.py"""
        return self.create_courier(payload)

    def login_courier(self, payload):
        url = f"{self.base_url}/courier/login"
        response = self.session.post(url, data=payload)
        return response

    def create_order(self, payload):
        url = f"{self.base_url}/orders"
        response = self.session.post(url, json=payload)
        return response

    def get_orders(self):
        url = f"{self.base_url}/orders"
        response = self.session.get(url)
        return response