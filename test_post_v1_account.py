import requests


def test_post_v1_account():
    # user register

    url = 'http://5.63.153.31:5051/v1/account'
    login = 'stas123456'
    password = '123456'

    json_data = {
        'login': {login},
        'email': f'{login}@mail.ru',
        'password': {password},
    }

    response = requests.post(url=url, json=json_data)
    print(response.status_code)
    print(response.text)


def test_get_api_v2_messages():
    # Getting registration messages via mail

    url = 'http://5.63.153.31:5025/api/v2/messages'

    params = {
        'limit': '50',
    }

    response = requests.get(url=url, params=params, verify=False)
    print(response.status_code)
    print(response.text)


def test_put_v1_account_token():
    # Getting token

    response = requests.put('http://5.63.153.31:5051/v1/account/a24cc2e9-5871-4612-866a-3b9ea5588cd1')
    print(response.status_code)
    print(response.text)


def test_v1_account_login():
    # User login

    json_data = {
        'login': 'stas123456',
        'rememberMe': True,
        'password': '123456',
    }

    response = requests.post('http://5.63.153.31:5051/v1/account/login', json=json_data)
    print(response.status_code)
    print(response.text)

