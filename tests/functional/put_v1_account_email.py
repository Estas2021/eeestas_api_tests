import time
# from faker import Faker
import json
import base64
import re

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi



def test_put_v1_account_email():


    account_api = AccountApi(host='http://5.63.153.31:5051')
    login_api = LoginApi(host='http://5.63.153.31:5051')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025')

    # fake = Faker()
    # fake_name = fake.name()

    login = 'fake_user012345678930'
    password = '1234567'
    email = f'{login}@mail.ru'

    # 1 register user

    json_data = {
        'login': login,
        'password': password,
        'email': email,
    }

    response = account_api.post_v1_account(json_data=json_data)

    assert response.status_code == 201, "Пользак не был зарегистрирован"

    # 2 get registration messages via email

    response = mailhog_api.get_api_v2_messages()

    assert response.status_code == 200, "Письма не были получены"

    # 3 get activation token
    token = get_activation_token_by_login(
        login,
        response
    )

    assert token is not None, f"Токен для пользака {login} не был получен"


    # 4 activate user
    response = account_api.put_v1_account_token(token)

    assert response.status_code == 200, f"Пользак {login} не был активирован"

    # 5 login user

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)

    assert response.status_code == 200, f"Пользак {login} не был авторизован"

    # 6 change user email
    json_data = {
        'login': login,
        'password': password,
        'email': f'changed_{login}@mail.ru'
    }

    response = account_api.put_v1_account_email(json_data=json_data)

    assert response.status_code == 200, "Имейл не был изменен"

    # 7 login user(403)
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)

    assert response.status_code == 403, f"Пользак {login} был авторизован"

    # 8 На почте находим токен по новому емейлу для подтверждения смены емейла
    response = mailhog_api.get_api_v2_messages(limit=1)


    changed_token = get_activation_token_by_login(
        login,
        response
    )
    print('\n'+ 'token: ', token)
    print('\n'+ 'changed_token: ', changed_token)

    assert changed_token is not None, f"НОВЫЙ токен для пользака {login} не был получен"

    # 9 Активируем этот токен
    response = account_api.put_v1_account_token(changed_token)

    assert response.status_code == 200, f"Пользак {login} не был активирован"

    # 10 Логинимся
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)

    assert response.status_code == 200, f"ПОВТОРНО Пользак не был авторизован!!!"



def get_activation_token_by_login(
        login,
        response
):
    """
    Get activation token from mailbox
    :param login:
    :param response:
    :return:
    """
    token = None

    for item in response.json()['items']:
        user_data = json.loads(item['Content']['Body'])
        user_login = user_data['Login']

        decoded_str = decode_mime(item['Content']['Headers']['Subject'][0])
        # print('\n'+ 'decoded_str: ', decoded_str)

        if user_login == login and login in decoded_str:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]

    return token


def decode_mime(
        encoded_string: str
) -> str:
    """
    Decode encoded Subject message from mailbox
    :param encoded_string:
    :return:
    """
    pattern = r"=\?utf-8\?b\?(.*?)\?="
    decoded_string = encoded_string

    for match in re.findall(pattern, encoded_string):
        decoded_part = base64.b64decode(match).decode("utf-8")
        decoded_string = decoded_string.replace(
            "=?utf-8?b?" + match + "?=", decoded_part
        )

    return decoded_string
