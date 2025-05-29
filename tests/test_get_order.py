import requests
import allure
from data import Urls,ErrorMessage

class TestGetOrder:
    @allure.title('Проверка получения заказов без авторизации')
    def test_get_order_without_auth(self):
        with allure.step('Отправка запроса на получения заказов без авторизации'):
            response = requests.get(f'{Urls.MAIN_URL}{Urls.API_CREATE_ORDERS}')
        with allure.step('Проверка,что код ответа 401 и получили сообщение об ошибке с текстом "You should be authorised"'):
            assert response.status_code == 401 and response.json()['message'] == ErrorMessage.TEXT_GET_ORDERS_NO_AUTH

    @allure.title('Проверка получения заказов с авторизацией')
    def test_get_order_with_auth(self,create_user_and_get_token,get_ingredient_hash):
        with allure.step('Авторизация пользователя и получение токена'):
            token = create_user_and_get_token
        with allure.step('Выборка ингредиентов для создания заказа'):
            ingredients = {'ingredients':[get_ingredient_hash['data'][0]['_id'],get_ingredient_hash['data'][2]['_id'],get_ingredient_hash['data'][7]['_id']]}
        with allure.step('Отправка запроса на создание заказа с ингредиентами'):
            requests.post(f'{Urls.MAIN_URL}{Urls.API_CREATE_ORDERS}', data=ingredients)
        with allure.step('Отправка запроса на получение заказов с авторизацией'):
            response = requests.get(f'{Urls.MAIN_URL}{Urls.API_CREATE_ORDERS}', headers={'Authorization': token})
        with allure.step('Проверка,что код ответа 200 и получили orders'):
            assert response.status_code == 200 and "orders" in response.text

