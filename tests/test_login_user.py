import requests
from data import Urls,ErrorMessage
from user_data import generate_user
import allure

class TestLoginUser:
    @allure.title('Проверка успешной авторизации пользователя')
    def test_login_user(self):
        payload = generate_user()
        requests.post(f'{Urls.MAIN_URL}{Urls.API_CREATE_USER}',data=payload)

        response = requests.post(f'{Urls.MAIN_URL}{Urls.API_LOGIN}',data=payload)
        assert response.status_code == 200 and response.json()['success'] == True

    @allure.title('Проверка неуспешной авторизации с неправильным паролем')
    def test_login_user_with_wrong_password(self):
        payload = generate_user()
        requests.post(f'{Urls.MAIN_URL}{Urls.API_CREATE_USER}',data=payload)
        payload['password'] = 'wrong password'
        response = requests.post(f'{Urls.MAIN_URL}{Urls.API_LOGIN}',data=payload)
        assert response.status_code == 401 and response.json()['message'] == ErrorMessage.TEXT_LOGIN_401
