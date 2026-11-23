# Sprint_7: тесты API Яндекс Самокат

Автотесты для эндпоинтов создания курьера, логина, заказа.

## Запуск
1. Активируй venv: `venv\Scripts\activate` (Windows) или `source venv/bin/activate` (macOS/Linux).
2. Установи зависимости: `pip install -r requirements.txt`.
3. Запусти тесты: `pytest`.
4. Сгенерируй отчёт Allure: `allure generate allure-results -o allure-report --clean`.

## Зависимости
- requests
- pytest
- allure-pytest

## Стенд
http://qa-scooter.praktikum-services.ru

## Отчёт
allure-report/