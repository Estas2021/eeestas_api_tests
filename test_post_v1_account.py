import requests


def test_post_v1_account():
    # register user

    login = 'stas1009ss'
    password = 'stas1009'
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
    print(response.status_code)
    print(response.text)


    # Getting token


    # activate user

    headers = {
        'accept': 'text/plain',
    }

    response = requests.put('http://5.63.153.31:5051/v1/account/552c9c40-0542-4981-b96c-6b65f117f339', headers=headers)
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

