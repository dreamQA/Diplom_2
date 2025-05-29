import pytest
import allure
import requests
from data import Urls,ErrorMessage
from user_data import generate_user

class TestCreateUser:
    @allure.title('Проверка успешного создания нового пользователя')
    def test_create_user(self):
        with allure.step('Генерация данных для пользователя'):
            payload = generate_user()
        with allure.step('Отправка запроса на создание пользователя'):
            response = requests.post(f'{Urls.MAIN_URL}{Urls.API_CREATE_USER}', data=payload)
        with allure.step('Получение ответа о успешном создании пользователя'):
            token = response.json()['accessToken']
        with allure.step('Удаляем созданного пользователя после теста'):
            requests.delete(f'{Urls.MAIN_URL}{Urls.API_DELETE_USER}',headers={'Authorization': token})
        with allure.step('Проверка,что пользователь успешно создался,код ответа 200 и получили accessToken'):
            assert response.status_code == 200 and 'accessToken' in response.text, (f'Ожидалось 200, получили {response.status_code}, \
                                                                                 ожидалось "accessToken", получили {response.text}')
    @allure.title('Проверка повторной регистрации пользователя')
    def test_create_user_double(self):
        with allure.step('Генерация данных для пользователя'):
            payload = generate_user()
        with allure.step('Отправка запроса на создание пользователя'):
            requests.post(f'{Urls.MAIN_URL}{Urls.API_CREATE_USER}', data=payload)
        with allure.step('Повторная отправка запроса на создание пользователя'):
            response = requests.post(f'{Urls.MAIN_URL}{Urls.API_CREATE_USER}', data=payload)
        with allure.step('Проверка,что код ответа 403 и получили сообщение об ошибке с текстом "User already exists"'):
            assert 403 == response.status_code and response.json()['message'] == ErrorMessage.TEXT_CREATE_403_DOUBLE

    @allure.title('Проверка регистрации пользователя без почты')
    def test_create_user_without_email(self):
        with allure.step('Генерация данных для пользователя'):
            payload = generate_user()
        with allure.step('Удаление сгенерированных данных почты'):
            del payload['email']
        with allure.step('Отправка запроса на создание пользователя без почты'):
            response = requests.post(f'{Urls.MAIN_URL}{Urls.API_CREATE_USER}', data={})
        with allure.step('Проверка,что код ответа 403 и получили сообщение об ошибке с текстом "Email, password and name are required fields"'):
            assert 403 == response.status_code and response.json()['message'] == ErrorMessage.TEXT_CREATE_403_WRONG

    @allure.title('Проверка регистрации пользователя без имени')
    def test_create_user_without_name(self):
        with allure.step('Генерация данных для пользователя'):
            payload = generate_user()
        with allure.step('Удаление сгенерированных данных имени'):
            del payload['name']
        with allure.step('Отправка запроса на создание пользователя без имени'):
            response = requests.post(f'{Urls.MAIN_URL}{Urls.API_CREATE_USER}', data={})
        with allure.step('Проверка,что код ответа 403 и получили сообщение об ошибке с текстом "Email, password and name are required fields"'):
            assert 403 == response.status_code and response.json()['message'] == ErrorMessage.TEXT_CREATE_403_WRONG

    @allure.title('Проверка регистрации пользователя без пароля')
    def test_create_user_without_password(self):
        with allure.step('Генерация данных для пользователя'):
            payload = generate_user()
        with allure.step('Удаление сгенерированных данных пароля'):
            del payload['password']
        with allure.step('Отправка запроса на создание пользователя без пароля'):
            response = requests.post(f'{Urls.MAIN_URL}{Urls.API_CREATE_USER}', data={})
        with allure.step( 'Проверка,что код ответа 403 и получили сообщение об ошибке с текстом "Email, password and name are required fields"'):
            assert 403 == response.status_code and response.json()['message'] == ErrorMessage.TEXT_CREATE_403_WRONG