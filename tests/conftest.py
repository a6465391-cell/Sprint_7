import sys
import os

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
import pytest
from utils.methods import register_new_courier_and_return_login_password

@pytest.fixture
def new_courier():
 
    credentials = register_new_courier_and_return_login_password()
    
    if not credentials:
        pytest.fail("Не удалось зарегистрировать тестового курьера для теста")

    yield credentials  
    pass 
