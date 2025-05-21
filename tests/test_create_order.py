import requests
import allure

from conftest import create_user_and_get_token
from data import Data,Urls,ErrorMessage,Burgers

class TestCreateOrder:
    @allure.title ('Проверка создания заказа + авторизация')

    def test_create_order_with_auth(self,create_user_and_get_token,get_ingredient_hash):
        requests.post(f'{Urls.MAIN_URL}{Urls.API_LOGIN}',data= create_user_and_get_token)
        ingredients = {'ingredients':[get_ingredient_hash['data'][1]['_id'],get_ingredient_hash['data'][4]['_id'],get_ingredient_hash['data'][8]['_id']]}
        response = requests.post(f'{Urls.MAIN_URL}{Urls.API_CREATE_ORDERS}',data=ingredients)
        order = response.json()
        assert order['name'] == Burgers.SPICY_UNDEAD_CRATER_BURGER and order['success'] == True

    @allure.title("Проверка создания заказа без авторизации")
    def test_create_order_without_auth(self,get_ingredient_hash):
        ingredients = {'ingredients':[get_ingredient_hash['data'][1]['_id'],get_ingredient_hash['data'][3]['_id'],get_ingredient_hash['data'][6]['_id']]}
        response = requests.post(f'{Urls.MAIN_URL}{Urls.API_CREATE_ORDERS}',data=ingredients)
        order = response.json()
        assert order['name'] == Burgers.SPACE_UNDEAD_BIO_BURGER and order['success'] == True

    @allure.title('Проверка создания заказа без ингредиентов')
    def test_create_order_without_ingredients(self,get_ingredient_hash):
        ingredients = {'ingredients':[]}
        response = requests.post(f'{Urls.MAIN_URL}{Urls.API_CREATE_ORDERS}',data=ingredients)
        assert response.status_code == 400 and response.json()['message'] == ErrorMessage.TEXT_CREATE_ORDER_WITHOUT_INGREDIENTS

    @allure.title('Проверка создания заказа с ингредиентами')
    def test_create_order_with_ingredients(self,create_user_and_get_token,get_ingredient_hash):
        ingredients = {'ingredients':[get_ingredient_hash['data'][0]['_id'],get_ingredient_hash['data'][2]['_id'],get_ingredient_hash['data'][7]['_id']]}
        response = requests.post(f'{Urls.MAIN_URL}{Urls.API_CREATE_ORDERS}',data=ingredients)
        order = response.json()
        assert order['name'] == Burgers.METEOR_FLY_CLASSIC_BURGER and order['success'] == True

    @allure.title('Проверка создания заказа с неверным хэш ингредиентов')
    def test_create_order_with_invalid_ingredients(self,get_ingredient_hash):
        ingredients = {'ingredients':[Data.f_hash,Data.f_hash]}
        response = requests.post(f'{Urls.MAIN_URL}{Urls.API_CREATE_ORDERS}',data=ingredients)
        assert response.status_code == 500
