import os
from superagi_client import Client


class AGIClientInitializer:
    def __init__(
        self,
        api_key: str = os.environ.get("SUPERAGI_API_KEY"),
        host: str = os.environ.get("SUPERAGI_HOST"),
    ) -> None:
        if not (isinstance(api_key, str) and isinstance(host, str)):
            raise TypeError("api_key and host must be of type str")

        self.api_key = api_key
        self.host = host
        self.client = None

    def get_client(self) -> Client:
        if self.client is None:
            self.client = Client(self.api_key, self.host)

        return self.client
