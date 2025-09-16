

class Configuration:
    def __init__(
            self,
            host: str,
            headers: dict = None,
            disable_log: bool = True
    ):
        """
        Для управления несколькими апи одновременно, вкл/выкл логов
        :param headers:
        :param host:
        :param disable_log:
        """
        self.host = host
        self.headers = headers
        self.disable_log = disable_log