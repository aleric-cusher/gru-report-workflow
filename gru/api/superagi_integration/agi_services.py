from .agi_client_initializer import AGIClientInitializer
from superagi_client import AgentConfig


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

    def _generate_agent_config(self) -> AgentConfig:
        pass

    def create_agent(self, data: dict) -> int:
        pass

    def run_agent(self, agent_id: int) -> int:
        pass

    def create_and_run_agent(self, data: dict) -> list[int, int]:
        pass

    def pause_agent(self, agent_id: int, run_id: int) -> None:
        pass

    def resume_agent(self, agent_id: int, run_id: int) -> None:
        pass

    def check_run_status(self, agent_id: int, run_id: int = None):
        pass
