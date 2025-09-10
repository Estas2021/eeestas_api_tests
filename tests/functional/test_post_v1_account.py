import json

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi


# from main import response_json


def test_post_v1_account():
    # register user

    account_api = AccountApi(host='http://5.63.153.31:5051')
    login_api = LoginApi(host='http://5.63.153.31:5051')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025')

    login = 'eeestas6'
    password = 'eeestas3'
    email = f'{login}@mail.ru'

    json_data = {
        'login': login,
        'password': password,
        'email': email,
    }

    response = account_api.post_v1_account(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 201, "Пользак не был зарегистрирован"

    # get registration messages via email

    response = mailhog_api.get_api_v2_messages()
    print('\n', response.status_code)
    print(response.text)
    assert response.status_code == 200, "Письма не были получены"

    # get activation token
    token = get_activation_token_by_login(login, response)

    assert token is not None, f"Токен для пользака {login} не был получен"

    # activate user
    response = account_api.put_v1_account_token(token)
    print(response.status_code)
    print(response.text)

    assert response.status_code == 200, f"Пользак {login} не был активирован"

    # login user

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f"Пользак {login} не был авторизован"



def get_activation_token_by_login(
        login,
        response
):
    token = None
    for item in response.json()['items']:
        user_data = json.loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            print('token: ', token)
    return token






