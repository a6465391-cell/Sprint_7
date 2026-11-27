import allure
from api.api_client import APIClient
from utils.methods import generate_random_string

@allure.epic("API Яндекс Самокат")
@allure.feature("Логин курьера")
class TestLogin:

    def setup_method(self):
        self.api_client = APIClient()

    @allure.story("Успешная авторизация")
    @allure.title("Курьер может авторизоваться с валидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_success(self, new_courier):
        login, password, _ = new_courier
        payload = {"login": login, "password": password}

        response = self.api_client.login_courier(payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, \
                f"Ожидался статус 200, получен {response.status_code}. Тело: {response.text}"

        with allure.step("Проверка наличия поля id в ответе"):
            data = response.json()
            assert "id" in data, f"В ответе отсутствует поле 'id': {data}"

    @allure.story("Авторизация с неверным паролем")
    @allure.title("Ошибка 404 при неверном пароле для существующего курьера")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_wrong_password(self, new_courier):
        login, password, _ = new_courier
        payload = {"login": login, "password": f"{password}_wrong"}

        response = self.api_client.login_courier(payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, \
                f"Ожидался 404, получен {response.status_code}. Тело: {response.text}"

        with allure.step("Проверка сообщения об ошибке"):
            data = response.json()
            assert "message" in data, f"В теле ответа нет сообщения об ошибке: {data}"

    @allure.story("Авторизация без пароля")
    @allure.title("Ошибка 400 при отсутствии пароля в запросе")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_missing_password(self, new_courier):
        login, _, _ = new_courier
        payload = {"login": login}

        response = self.api_client.login_courier(payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 400, \
                f"Ожидался 400, получен {response.status_code}. Тело: {response.text}"

        with allure.step("Проверка сообщения об ошибке"):
            data = response.json()
            assert "message" in data, f"В теле ответа нет сообщения об ошибке: {data}"

    @allure.story("Авторизация без логина")
    @allure.title("Ошибка 400 при отсутствии логина в запросе")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_missing_login(self, new_courier):
        _, password, _ = new_courier
        payload = {"password": password}

        response = self.api_client.login_courier(payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 400, \
                f"Ожидался 400, получен {response.status_code}. Тело: {response.text}"

        with allure.step("Проверка сообщения об ошибке"):
            data = response.json()
            assert "message" in data, f"В теле ответа нет сообщения об ошибке: {data}"

    @allure.story("Авторизация несуществующего курьера")
    @allure.title("Ошибка 404 при логине несуществующего курьера")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_non_existent_user(self):
        payload = {"login": f"no_such_{generate_random_string(8)}", "password": "any_password"}

        response = self.api_client.login_courier(payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, \
                f"Ожидался 404, получен {response.status_code}. Тело: {response.text}"

        with allure.step("Проверка сообщения об ошибке"):
            data = response.json()
            assert "message" in data, f"В теле ответа нет сообщения об ошибке: {data}"
