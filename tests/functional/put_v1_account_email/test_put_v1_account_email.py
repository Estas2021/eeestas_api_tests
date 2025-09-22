

def test_put_v1_account_email(account_helper, create_user):
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


    # 6 change user email
    # 7 login user(403)
    # 8 На почте находим токен по новому емейлу для подтверждения смены емейла
    # 9 Активируем этот токен
    account_helper.change_registered_user_email(login=login, password=password)

    # 10 Логинимся
    account_helper.login_user(login=login, password=password)



