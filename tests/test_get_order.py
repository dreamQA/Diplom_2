import requests
import allure
from data import Urls,ErrorMessage

class TestGetOrder:
    @allure.title('Проверка получения заказов без авторизации')
    def test_get_order_without_auth(self):
        response = requests.get(f'{Urls.MAIN_URL}{Urls.API_CREATE_ORDERS}')
        assert response.status_code == 401 and response.json()['message'] == ErrorMessage.TEXT_GET_ORDERS_NO_AUTH

    @allure.title('Проверка получения заказов с авторизацией')
    def test_get_order_with_auth(self,create_user_and_get_token,get_ingredient_hash):
        token = create_user_and_get_token
        ingredients = {'ingredients':[get_ingredient_hash['data'][0]['_id'],get_ingredient_hash['data'][2]['_id'],get_ingredient_hash['data'][7]['_id']]}
        requests.post(f'{Urls.MAIN_URL}{Urls.API_CREATE_ORDERS}', data=ingredients)
        response = requests.get(f'{Urls.MAIN_URL}{Urls.API_CREATE_ORDERS}', headers={'Authorization': token})
        assert response.status_code == 200 and "orders" in response.text

