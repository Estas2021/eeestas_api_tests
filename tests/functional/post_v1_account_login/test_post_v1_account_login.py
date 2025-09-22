

def test_post_v1_account_login(account_helper, create_user):
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
