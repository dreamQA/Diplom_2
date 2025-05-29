import requests
from data import Urls,ErrorMessage
from user_data import generate_user
import allure

class TestLoginUser:
    @allure.title('Проверка успешной авторизации пользователя')
    def test_login_user(self):
        with allure.step('Генерация данных пользователя'):
            payload = generate_user()
        with allure.step('Отправка запроса на создание пользователя'):
            requests.post(f'{Urls.MAIN_URL}{Urls.API_CREATE_USER}',data=payload)
        with allure.step('Авторизация пользователя'):
            response = requests.post(f'{Urls.MAIN_URL}{Urls.API_LOGIN}',data=payload)
        with allure.step('Проверка,что код ответа 200 и что авторизация прошла успешно'):
            assert response.status_code == 200 and response.json()['success'] == True

    @allure.title('Проверка неуспешной авторизации с неправильным паролем')
    def test_login_user_with_wrong_password(self):
        with allure.step('Генерация данных пользователя'):
            payload = generate_user()
        with allure.step('Отправка запроса на создание пользователя'):
            requests.post(f'{Urls.MAIN_URL}{Urls.API_CREATE_USER}',data=payload)
        with allure.step('Подмена пароля на неправильный после создания'):
            payload['password'] = 'wrong password'
        with allure.step('Авторизация пользователя с некорректным паролем'):
            response = requests.post(f'{Urls.MAIN_URL}{Urls.API_LOGIN}',data=payload)
        with allure.step('Проверка,что код ответа 401 и получили сообщение об ошибке с текстом "email or password are incorrect"'):
            assert response.status_code == 401 and response.json()['message'] == ErrorMessage.TEXT_LOGIN_401
