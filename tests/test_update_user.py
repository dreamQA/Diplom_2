import requests
import pytest
from data import Data,Urls,ErrorMessage
import allure

class TestUpdateUser:
    @allure.title('Проверка успешного обновления данных пользователя')
    @pytest.mark.parametrize('update_argument,update_data', (['name',Data.login],['email', Data.email]))
    def test_update_user_data_success(self, update_argument, update_data, create_user_and_get_token):
        with allure.step('Авторизация и получение текущих данных пользователя'):
            user_data_response = requests.get(f'{Urls.MAIN_URL}{Urls.API_GET_USER}', headers = {'Authorization': create_user_and_get_token})
        with allure.step('Перевод данных в читаемый формат json'):
            user_data = user_data_response.json()
        with allure.step('Обновление поля пользователя'):
            user_data['user'][update_argument] = update_data
        with allure.step('Авторизация и отправка запроса на обновление данных пользователя'):
            update_user = requests.patch(f'{Urls.MAIN_URL}{Urls.API_GET_USER}', json=user_data, headers = {'Authorization': create_user_and_get_token})
        with allure.step('Проверка,что код ответа 200 и данные обновились'):
            assert update_user.status_code == 200 and update_user.json()['success'] == True

    @allure.title('Проверка обновления данных пользователя без авторизации')
    def test_update_user_data_no_auth_failed(self, create_user_and_get_token):
        with allure.step('Получение данных пользователя'):
            user_data = requests.get(f'{Urls.MAIN_URL}{Urls.API_GET_USER}', headers = {'Authorization': create_user_and_get_token})
        with allure.step('Изменение имени пользователя'):
            user_data.json()['user']['name'] = Data.login
        with allure.step('Отправка запроса на обновление данных пользователя без авторизации'):
            update_user = requests.patch(f'{Urls.MAIN_URL}{Urls.API_GET_USER}', data = user_data)
        with allure.step('Проверка,что код ответа 401 и получили сообщение об ошибке с текстом "You should be authorised"'):
            assert update_user.status_code == 401 and update_user.json()['message'] == ErrorMessage.TEXT_UPDATE_401
