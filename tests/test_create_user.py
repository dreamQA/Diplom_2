import pytest
import allure
import requests
from data import Urls,ErrorMessage
from user_data import generate_user

class TestCreateUser:
    @allure.title('Проверка успешного создания нового пользователя')
    def test_create_user(self):
        payload = generate_user()
        response = requests.post(f'{Urls.MAIN_URL}{Urls.API_CREATE_USER}', data=payload)
        token = response.json()['accessToken']
        requests.delete(f'{Urls.MAIN_URL}{Urls.API_DELETE_USER}',headers={'Authorization': token})
        assert response.status_code == 200 and 'accessToken' in response.text, (f'Ожидалось 200, получили {response.status_code}, \
                                                                                 ожидалось "accessToken", получили {response.text}')
    @allure.title('Проверка повторной регистрации пользователя')
    def test_create_user_double(self):
        payload = generate_user()
        requests.post(f'{Urls.MAIN_URL}{Urls.API_CREATE_USER}', data=payload)
        response = requests.post(f'{Urls.MAIN_URL}{Urls.API_CREATE_USER}', data=payload)
        assert 403 == response.status_code and response.json()['message'] == ErrorMessage.TEXT_CREATE_403_DOUBLE

    @allure.title('Проверка регистрации пользователя без почты')
    def test_create_user_without_email(self):
        payload = generate_user()
        del payload['email']
        response = requests.post(f'{Urls.MAIN_URL}{Urls.API_CREATE_USER}', data={})
        assert 403 == response.status_code and response.json()['message'] == ErrorMessage.TEXT_CREATE_403_WRONG

    @allure.title('Проверка регистрации пользователя без имени')
    def test_create_user_without_name(self):
        payload = generate_user()
        del payload['name']
        response = requests.post(f'{Urls.MAIN_URL}{Urls.API_CREATE_USER}', data={})
        assert 403 == response.status_code and response.json()['message'] == ErrorMessage.TEXT_CREATE_403_WRONG

    @allure.title('Проверка регистрации пользователя без пароля')
    def test_create_user_without_password(self):
        payload = generate_user()
        del payload['password']
        response = requests.post(f'{Urls.MAIN_URL}{Urls.API_CREATE_USER}', data={})
        assert 403 == response.status_code and response.json()['message'] == ErrorMessage.TEXT_CREATE_403_WRONG