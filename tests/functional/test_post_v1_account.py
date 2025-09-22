from datetime import datetime
from collections import namedtuple

import pytest

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

@pytest.fixture
def account_api():
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    return account

@pytest.fixture
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    mailhog = MailHogApi(configuration=mailhog_configuration)
    return mailhog

@pytest.fixture
def account_helper(account_api, mailhog_api):
    account_helper = AccountHelper(dm_api_account=account_api,mailhog=mailhog_api)
    return account_helper


@pytest.fixture
def create_user():
    now = datetime.now()
    data = now.strftime("%d_%m_%Y_%H_%M_%S")
    login = f'NIGHT_RISER_{data}'
    password = '1234567'
    email = f'{login}@mail.ru'

    User = namedtuple('User', ['login', 'password', 'email'])
    user = User(login=login, password=password, email=email)
    return user


def test_post_v1_account(account_helper, create_user):
    login = create_user.login
    password = create_user.password
    email = create_user.email


    # 1 register new user
    account_helper.register_new_user(
        login=login,
        password=password,
        email=email
    )

    # 2 login user
    account_helper.login_user(login=login, password=password)
