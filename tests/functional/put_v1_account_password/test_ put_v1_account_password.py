"""
в файле put_v1_account_password:

        - Регистрация пользователя

        - Авторизация пользователя

        - Смена пароля с пробросом авторизационного токена в хэдэры и указанием токена для сброса пароля из письма

        - Авторизация пользователя с новым паролем
"""


def test_put_v1_account_password(
        account_helper,
        create_user
):

    login = create_user.login,
    password = create_user.password,
    email = create_user.email

    # 1 Регистрация пользователя
    account_helper.register_new_user(
        login=login,
        password=password,
        email=email
    )

    # 2 Авторизация пользователя
    account_helper.login_user(
        login=login,
        password=password
    )

    # 3 Смена пароля
    #  а) с пробросом авторизационного токена в хэдэры
    #  б) и указанием токена для сброса пароля из письма
