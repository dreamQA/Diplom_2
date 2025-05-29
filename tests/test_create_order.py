import requests
import allure

from conftest import create_user_and_get_token
from data import Data,Urls,ErrorMessage,Burgers

class TestCreateOrder:
    @allure.title ('Проверка создания заказа + авторизация')

    def test_create_order_with_auth(self,create_user_and_get_token,get_ingredient_hash):
        with allure.step('Авторизация пользователя'):
            requests.post(f'{Urls.MAIN_URL}{Urls.API_LOGIN}',data= create_user_and_get_token)
        with allure.step('Выборка ингредиентов для создания заказа'):
            ingredients = {'ingredients':[get_ingredient_hash['data'][1]['_id'],get_ingredient_hash['data'][4]['_id'],get_ingredient_hash['data'][8]['_id']]}
        with allure.step('Отправка запроса на создание заказа с ингредиентами'):
            response = requests.post(f'{Urls.MAIN_URL}{Urls.API_CREATE_ORDERS}',data=ingredients)
        with allure.step('Получение ответа на создание заказа'):
            order = response.json()
        with allure.step('Проверка,что имя "Spicy бессмертный краторный бургер" и заказ создался и код ответа 200'):
            assert order['name'] == Burgers.SPICY_UNDEAD_CRATER_BURGER and order['success'] == True and response.status_code == 200

    @allure.title("Проверка создания заказа без авторизации")
    def test_create_order_without_auth(self,get_ingredient_hash):
        with allure.step('Выборка ингредиентов для создания заказа'):
            ingredients = {'ingredients':[get_ingredient_hash['data'][1]['_id'],get_ingredient_hash['data'][3]['_id'],get_ingredient_hash['data'][6]['_id']]}
        with allure.step('Отправка запроса на создание заказа с ингредиентами'):
            response = requests.post(f'{Urls.MAIN_URL}{Urls.API_CREATE_ORDERS}',data=ingredients)
        with allure.step('Получение ответа на создание заказа'):
            order = response.json()
        with allure.step('Проверка,что имя "Space бессмертный био-марсианский бургер" и заказ создался  и код ответа 200'):
            assert order['name'] == Burgers.SPACE_UNDEAD_BIO_BURGER and order['success'] == True and response.status_code == 200

    @allure.title('Проверка создания заказа без ингредиентов')
    def test_create_order_without_ingredients(self,get_ingredient_hash):
        with allure.step('Собираем заказ без ингредиентов'):
            ingredients = {'ingredients':[]}
        with allure.step('Отправка запроса на создание заказа'):
            response = requests.post(f'{Urls.MAIN_URL}{Urls.API_CREATE_ORDERS}',data=ingredients)
        with allure.step('Проверяем что код ответа 400 и сообщение об ошибке с текстом: "Ingredient ids must be provided"'):
            assert response.status_code == 400 and response.json()['message'] == ErrorMessage.TEXT_CREATE_ORDER_WITHOUT_INGREDIENTS

    @allure.title('Проверка создания заказа с ингредиентами')
    def test_create_order_with_ingredients(self,create_user_and_get_token,get_ingredient_hash):
        with allure.step('Выборка ингредиентов для создания заказа'):
            ingredients = {'ingredients':[get_ingredient_hash['data'][0]['_id'],get_ingredient_hash['data'][2]['_id'],get_ingredient_hash['data'][7]['_id']]}
        with allure.step('Отправка запроса на создание заказа с ингредиентами'):
            response = requests.post(f'{Urls.MAIN_URL}{Urls.API_CREATE_ORDERS}',data=ingredients)
        with allure.step('Получение ответа на создание заказа'):
            order = response.json()
        with allure.step('Проверка,что имя  "Метеоритный флюоресцентный традиционный-галактический бургер" и заказ создался и код ответа 200'):
         assert order['name'] == Burgers.METEOR_FLY_CLASSIC_BURGER and order['success'] == True and response.status_code == 200

    @allure.title('Проверка создания заказа с неверным хэш ингредиентов')
    def test_create_order_with_invalid_ingredients(self,get_ingredient_hash):
        with allure.step('Выборка ингредиентов с неверным хэш'):
            ingredients = {'ingredients':[Data.f_hash,Data.f_hash]}
        with allure.step('Отправка запроса на создание заказа с неверным хэш'):
            response = requests.post(f'{Urls.MAIN_URL}{Urls.API_CREATE_ORDERS}',data=ingredients)
        with allure.step('Проверка,что код ответа 500'):
            assert response.status_code == 500
