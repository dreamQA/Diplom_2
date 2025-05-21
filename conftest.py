import pytest
import time
import requests
from data import Urls
from user_data import generate_user

@pytest.fixture()
def get_ingredient_hash():
    response = requests.get(f'{Urls.MAIN_URL}{Urls.API_GET_INGREDIENTS}')
    ingredients = response.json()
    return ingredients

@pytest.fixture()
def create_user_and_get_token(timeout=10):
    start_time = time.time()  # Запоминаем время начала
    try:
        # Генерация данных для нового пользователя
        payload = generate_user()
        print("Payload for user creation:", payload)  # Вывод данных

        # Создание нового пользователя
        create_response = requests.post(f'{Urls.MAIN_URL}{Urls.API_CREATE_USER}', data=payload)
        if not create_response.ok:
            print(f"Failed to create user: {create_response.status_code} - {create_response.text}")
        create_response.raise_for_status()  # Проверка ответного кода на ошибки

        # Удаление имени для данных аутентификации
        auth_payload = {key: value for key, value in payload.items() if key != 'name'}

        # Аутентификация пользователя с условным таймером
        while True:
            login_response = requests.post(f'{Urls.MAIN_URL}{Urls.API_LOGIN}', data=auth_payload)
            if login_response.ok:  # Успешный ответ
                response_data = login_response.json()
                if 'accessToken' in response_data:
                    token = response_data['accessToken']
                    yield token
                    break
            if time.time() - start_time > timeout:
                raise TimeoutError("Не удалось получить токен за отведенное время.")
            time.sleep(1)  # Ожидание 1 секунду перед повтором запроса

    finally:
        # Удаление пользователя после использования токена
        if 'token' in locals():  # Проверка наличия токена
            requests.delete(f'{Urls.MAIN_URL}{Urls.API_DELETE_USER}', headers={'Authorization': token})









