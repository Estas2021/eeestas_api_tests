import json
import base64
import re

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
from helpers.account_helper import AccountHelper
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            sort_keys=True
        )
    ]
)


def test_post_v1_account():
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_api_account=account,mailhog=mailhog)

    login = 'late_nighter_2009'
    password = '1234567'
    email = f'{login}@mail.ru'

    # register new user
    account_helper.register_new_user(
        login=login,
        password=password,
        email=email
    )

    # 5 login user
    account_helper.login_user(login=login, password=password)



# def get_activation_token_by_login(
#         login,
#         response
# ):
#     """
#     Get activation token from mailbox
#     :param login:
#     :param response:
#     :return:
#     """
#     token = None
#
#     for item in response.json()['items']:
#         user_data = json.loads(item['Content']['Body'])
#         user_login = user_data['Login']
#
#         decoded_str = decode_mime(item['Content']['Headers']['Subject'][0])
#         # print('\n'+ 'decoded_str: ', decoded_str)
#
#         if user_login == login and login in decoded_str:
#             token = user_data['ConfirmationLinkUrl'].split('/')[-1]
#
#     return token
#
#
# def decode_mime(
#         encoded_string: str
# ) -> str:
#     """
#     Decode encoded Subject message from mailbox
#     :param encoded_string:
#     :return:
#     """
#     pattern = r"=\?utf-8\?b\?(.*?)\?="
#     decoded_string = encoded_string
#
#     for match in re.findall(pattern, encoded_string):
#         decoded_part = base64.b64decode(match).decode("utf-8")
#         decoded_string = decoded_string.replace(
#             "=?utf-8?b?" + match + "?=", decoded_part
#         )
#
#     return decoded_string
