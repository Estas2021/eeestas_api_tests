from restclient.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(
            self,
            json_data
    ):
        """
        Register new user
        :param json_data:
        :return:
        """
        response = self.post(           # больше не исп-ем requests, rest_client исп-ем
            path='/v1/account',
            json=json_data
        )
        return response

    def get_v1_account(
            self,
            **kwargs
    ):
        """
        Get current user
        :param
        :return:
        """
        response = self.get(
            path='/v1/account',
            **kwargs
        )
        return response

    def put_v1_account_token(
            self,
            token
    ):
        """
        Activate registered user using token
        :param token:
        :return:
        """

        response = self.put(
            path=f'/v1/account/{token}'
        )
        return response

    def put_v1_account_email(
            self,
            json_data
    ):
        """
        Change registered user email
        :param json_data:
        :return:
        """
        response = self.put(
            path='/v1/account/email',
            json=json_data
        )
        return response

    def put_v1_account_password(
            self,
            json_data
    ):
        """
        Reset registered user password
        :param json_data:
        :return:
        """
        response = self.put(
            path='/v1/account/password',
            json=json_data
        )
        return response