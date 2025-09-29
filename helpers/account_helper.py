import base64
import json
import re

from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
from retrying import retry


def retry_if_result_none(
        result
):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None


def decode_mime(
        encoded_string: str,
):
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


# def retry_getting_token(
#         func
# ):
#     def wrapper(
#             *args,
#             **kwargs
#     ):
#         token = None
#         count = 0
#         while token is None:
#             token = func(*args, **kwargs)
#             print(f"Попытка получения активационного токена номер {count}..")
#             count += 1
#
#             if count == 5:
#                 raise AssertionError("Превышено кол-во получения активационного токена")
#             if token:
#                 return token
#
#             time.sleep(1)
#
#     return wrapper


class AccountHelper:

    def __init__(
            self,
            dm_api_account: DMApiAccount,
            mailhog: MailHogApi
    ):
        self.dm_api_account = dm_api_account
        self.mailhog = mailhog


    def auth_client(
            self,
            login: str,
            password: str
    ):
        response = self.dm_api_account.login_api.post_v1_account_login(
            json_data={
                "login":login,
                "password":password
            }
        )

        token = {
            "x-dm-auth-token": response.headers["x-dm-auth-token"]
        }

        self.dm_api_account.account_api.set_headers(token)
        self.dm_api_account.login_api.set_headers(token)


    def register_new_user(
            self,
            login: str,
            password: str,
            email: str,
    ):
        json_data = {
            'login': login,
            'password': password,
            'email': email,
        }

        response = self.dm_api_account.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, "Пользак не был зарегистрирован"

        token = self.get_activation_token_by_login(login=login)
        print('\n' + 'token: ', token)
        assert token is not None, f"Токен для пользака {login} не был получен"

        response = self.dm_api_account.account_api.put_v1_account_token(token)
        assert response.status_code == 200, f"Пользак {login} не был активирован"

        return response


    def login_user(
            self,
            login: str,
            password: str,
            remember_me: bool = True
    ):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': True,
        }

        response = self.dm_api_account.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 200, f"Пользак {login} не был авторизован"

        return response


    def change_registered_user_email(
            self,
            login: str,
            password: str

    ):
        json_data = {
            'login': login,
            'password': password,
            'email': f'changed_{login}@mail.ru'
        }

        response = self.dm_api_account.account_api.put_v1_account_email(json_data=json_data)
        assert response.status_code == 200, "Имейл не был изменен"

        json_data = {
            'login': login,
            'password': password,
            'rememberMe': True,
        }

        response = self.dm_api_account.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 403, f"Пользак {login} был авторизован"

        changed_token = self.get_activation_token_by_login(login=login)

        print('\n' + 'changed_token: ', changed_token)
        assert changed_token is not None, f"Токен для пользака {login} не был получен"

        response = self.dm_api_account.account_api.put_v1_account_token(changed_token)
        assert response.status_code == 200, f"Пользак {login} не был активирован"

        return response




    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_activation_token_by_login(
            self,
            login,
    ):
        """
        Get activation token from mailbox
        :param login:
        :return:
        """
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages(limit=1)
        for item in response.json()['items']:
            user_data = json.loads(item['Content']['Body'])
            user_login = user_data['Login']

            decoded_str = decode_mime(item['Content']['Headers']['Subject'][0])
            # print('\n'+ 'decoded_str: ', decoded_str)

            if user_login == login and login in decoded_str:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]

        return token
