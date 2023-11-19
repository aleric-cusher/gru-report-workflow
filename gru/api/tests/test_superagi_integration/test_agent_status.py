from django.test import SimpleTestCase
from api.superagi_integration.agent_status import AgentStatus


class TestAgentStatusEnum(SimpleTestCase):
    def test_map_known_status(self):
        status_dict = {"status": "COMPLETED"}
        status_str = status_dict.get("status", "").upper()
        agent_status = AgentStatus[status_str]
        self.assertEqual(agent_status, AgentStatus.COMPLETED)

    def test_handle_unknown_status(self):
        unknown_status_dict = {"status": "UNKNOWN_STATUS"}
        unknown_status_str = unknown_status_dict.get("status", "").upper()
        with self.assertRaises(KeyError):
            unknown_agent_status = AgentStatus[unknown_status_str]

    def test_display_status_information(self):
        status_dict = {"status": "RUNNING"}
        status_str = status_dict.get("status", "").upper()
        agent_status = AgentStatus[status_str]
        self.assertEqual(agent_status, AgentStatus.RUNNING)
        self.assertEqual(agent_status.name, "RUNNING")
