from .agi_client_initializer import AGIClientInitializer


class AGIServices:
    def __init__(
        self,
        client_initializer_instance: AGIClientInitializer,
    ) -> None:
        if not isinstance(client_initializer_instance, AGIClientInitializer):
            raise TypeError(
                "client_initializer_instance must be of type AGIClientInitializer"
            )

        self.client = client_initializer_instance.get_client()
