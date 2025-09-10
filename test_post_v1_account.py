import pprint
import json
import requests

# from main import response_json


def test_post_v1_account():
    # register user

    login = 'eeestas1'
    password = 'eeestas1'
    email = f'{login}@mail.ru'

    json_data = {
        'login': login,
        'password': password,
        'email': email,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account', json=json_data)
    print(response.status_code)
    print(response.text)

    # get registration messages via email

    params = {
        'limit': '50',
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params, verify=False)
    print('\n', response.status_code)
    # print(response.text)
    # pprint.pprint(response.json())



    # get token
    for item in response.json()['items']:
        user_data = json.loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            print('token: ', token)

    # activate user
    headers = {
        'accept': 'text/plain',
    }

    response = requests.put(f'http://5.63.153.31:5051/v1/account/{token}', headers=headers)
    print(response.status_code)
    print(response.text)

    # login

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account/login', headers=headers, json=json_data)
    print(response.status_code)
    print(response.text)
