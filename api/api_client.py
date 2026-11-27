import requests
import allure


class APIClient:
    def __init__(self, base_url="https://qa-scooter.praktikum-services.ru/api/v1"):
        self.base_url = base_url
        self.session = requests.Session()

    @allure.step("Создание курьера")
    def create_courier(self, payload):
        response = self.session.post(f"{self.base_url}/courier", data=payload)
        return response

    @allure.step("Авторизация курьера")
    def login_courier(self, payload):
        response = self.session.post(f"{self.base_url}/courier/login", json=payload)
        return response

    @allure.step("Получение id курьера")
    def get_courier_id(self, login, password):
        response = self.login_courier({"login": login, "password": password})
        if response.status_code == 200:
            return response.json().get("id")
        return None

    @allure.step("Удаление курьера")
    def delete_courier(self, courier_id):
        if not courier_id:
            return None

        response = self.session.delete(f"{self.base_url}/courier/{courier_id}")
        return response


    @allure.step("Создание заказа")
    def create_order(self, payload):
        response = self.session.post(f"{self.base_url}/orders", json=payload)
        return response

    @allure.step("Отмена заказа")
    def cancel_order(self, track):
        response = self.session.put(
            f"{self.base_url}/orders/cancel",
            data={"track": track}
        )
        return response


    @allure.step("Получение списка заказов")
    def get_orders(self, limit=10, page=0, **filters):
        params = {"limit": limit, "page": page}
        params.update(filters)
        response = self.session.get(f"{self.base_url}/orders", params=params)
        return response
