import base64
import json
import re

from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi

def decode_mime(
            encoded_string: str
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

class AccountHelper:
    def __init__(
            self,
            dm_api_account: DMApiAccount,
            mailhog: MailHogApi
    ):
        self.dm_api_account = dm_api_account
        self.mailhog = mailhog


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

        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не были получены"

        token = self.get_activation_token_by_login(login=login, response=response)
        assert token is not None, f"Токен для пользака {login} не был получен"

        response = self.dm_api_account.account_api.put_v1_account_token(token)
        assert response.status_code == 200, f"Пользак {login} не был активирован"

        return response


    def login_user(
            self,
            login: str,
            password: str,
            remember_me: bool=True
    ):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': True,
        }

        response = self.dm_api_account.login_api.post_v1_account_login(json_data=json_data)

        assert response.status_code == 200, f"Пользак {login} не был авторизован"

        return response



    @staticmethod
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



