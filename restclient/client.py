from requests import (
    session,
    JSONDecodeError,
)

import structlog
import uuid


class RestClient:
    def __init__(
            self,
            host,
            headers = None
    ):
        self.host = host
        self.headers = headers
        self.session = session()                                        # зачем нужен session??
        self.log = structlog.get_logger(__name__).bind(service='api')   # инициализация лога
        #                                           ----^-----
        # bind(service='api') <-- в названии может быть bd, grpc

    def post(
            self,
            path,
            **kwargs
    ):
        return self._send_request(method='POST', path=path, **kwargs)

    def get(
            self,
            path,
            **kwargs
    ):
        return self._send_request(method='GET', path=path, **kwargs)

    def put(
            self,
            path,
            **kwargs
    ):
        return self._send_request(method='PUT', path=path, **kwargs)

    def delete(
            self,
            path,
            **kwargs
    ):
        return self._send_request(method='DELETE', path=path, **kwargs)


    def _send_request(
            self,
            method,
            path,
            **kwargs
    ):
        # нужно получить идентификатор для каждого запроса
        log = self.log.bind(event_id=str(uuid.uuid4()))
        full_url = self.host + path

        log.msg(
            event='Request',
            method=method,
            full_url=full_url,
            headers=kwargs.get('headers'),
            params=kwargs.get('params'),
            json=kwargs.get('json'),
            data=kwargs.get('data')
        )
        # оборачиваем нашу библиотеку requests для отправки запросов и получения ответов
        rest_response = self.session.request(method=method, url=full_url,**kwargs)

        log.msg(
            event='Response',
            status_code=rest_response.status_code,
            headers=rest_response.headers,
            # json=rest_response.json()
            json=self._get_response_json(rest_response)
        )

        return rest_response

    # значит функция не исп-ет функции и параметры, которые внутри класса r_r
    @staticmethod
    def _get_response_json(
            rest_response
    ):
        try:
            return rest_response.json()
        except JSONDecodeError:
            return {}