# tests/conftest.py
import sys
import os

# Добавляем корень проекта в путь поиска модулей
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import pytest
from utils.methods import register_new_courier_and_return_login_password

@pytest.fixture
def new_courier():
    credentials = register_new_courier_and_return_login_password()
    if not credentials:
        pytest.skip("Не удалось зарегистрировать курьера")
    return credentials
