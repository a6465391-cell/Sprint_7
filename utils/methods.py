import string
import random
from api.api_client import APIClient

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def register_new_courier_and_return_login_password():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    api_client = APIClient()  
    try:
        response = api_client.register_courier(payload)
    except Exception as e:
        print(f"❌ Ошибка соединения при регистрации: {e}")
        return []

    if response.status_code != 201:
        print(f"⚠️ Регистрация не удалась! Статус: {response.status_code}")
        print(f"Тело ответа: {response.text}")
        print(f"Отправленные данные: {payload}")
        return []

    return [login, password, first_name]