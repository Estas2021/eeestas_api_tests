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

    login = 'esv1909999998722222'
    password = '1234567'
    email = f'{login}@mail.ru'

    # 1 register new user
    account_helper.register_new_user(
        login=login,
        password=password,
        email=email
    )

    # 2 login user
    account_helper.login_user(login=login, password=password)


    # 6 change user email
    # 7 login user(403)
    # 8 На почте находим токен по новому емейлу для подтверждения смены емейла
    # 9 Активируем этот токен
    account_helper.change_registered_user_email(login=login, password=password)

    # 10 Логинимся
    account_helper.login_user(login=login, password=password)



