# utils/methods.py
import requests
import random
import string
from config.config import BASE_URL

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

    # Важно: json= и http://
    response = requests.post(f"{BASE_URL}/api/v1/courier", json=payload)

    if response.status_code == 201:
        return [login, password, first_name]
    return []