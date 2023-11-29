from typing import Any
from unittest.mock import MagicMock, patch, call
from django.test import TestCase
from django.db.models.signals import pre_save, post_save

from api.signals import on_contact_lead_save, on_superagi_run_complete_update
from api.tasks import (
    add_agent_workflow,
    handle_workflow_statuses,
    process_and_email_report,
)
from api.models import ContactLeads
from api.utils import logger

from superagi_client import AgentRunFilter


class MockClient(MagicMock):
    def __init__(self, *args: Any, **kw: Any) -> None:
        super().__init__(*args, **kw)

    def _get_agent_run_status_side_effect(self, *args, **kwargs):
        if args[0] == 1:
            return {"status": "COMPLETED"}
        if args[0] == 2:
            return {"status": "PAUSED"}
        raise Exception("Unexpected call")  # pragma: no cover

    def _get_agent_run_resources_side_effect(self, *args, **kwargs):
        agent_run_ids = kwargs.get("agent_run_ids", None)
        if agent_run_ids == [1]:
            return {"1": ["http://test.resource/url.txt"]}
        raise Exception("Unexpected call")  # pragma: no cover

    def _resume_agent_side_effect(self, *args, **kwargs):
        agent_id = kwargs.get("agent_id", None)
        agent_run_ids = kwargs.get("agent_run_ids", None)
        if agent_id == 2 and agent_run_ids == [2]:
            return {"result": "success"}
        raise Exception("Unexpected call")  # pragma: no cover

    def _create_agent_side_effect(self, *args, **kwargs):
        agent_config = kwargs.get("agent_config", None)
        if agent_config is not None:
            return {"agent_id": 3}
        raise Exception("Unexpected call")  # pragma: no cover

    def _create_agent_run_side_effect(self, *args, **kwargs):
        if args[0] == 3:
            return {"run_id": 4}
        raise Exception("Unexpected call")  # pragma: no cover


class TestCeleryTasksWorkflow(TestCase):
    def setUp(self):
        pre_save.disconnect(on_superagi_run_complete_update, sender=ContactLeads)
        post_save.disconnect(on_contact_lead_save, sender=ContactLeads)

    @patch("api.superagi_integration.agi_client_initializer.Client")
    def test_add_agent_workflow(self, mock_superagi_client):
        mock_client_instance = MockClient()
        mock_superagi_client.return_value = mock_client_instance

        mock_client_instance.create_agent.side_effect = (
            mock_client_instance._create_agent_side_effect
        )
        mock_client_instance.create_agent_run.side_effect = (
            mock_client_instance._create_agent_run_side_effect
        )

        data1 = {
            "name": "test",
            "email": "test@test.com",
            "phone": "1234567890",
            "message": "message",
            "industry": "Furniture",
            "company_website": "https://www.companywebsite.com",
            "goals": "goals",
            "company_name": "Company Name",
        }

        contact_lead = ContactLeads.objects.create(**data1)

        add_agent_workflow(contact_lead.pk)

        contact_lead.refresh_from_db()
        self.assertEqual(contact_lead.agent_id, 3)
        self.assertEqual(contact_lead.run_id, 4)
        self.assertFalse(contact_lead.superagi_run_complete)

    @patch("api.superagi_integration.agi_client_initializer.Client")
    def test_handle_workflow_statuses(self, mock_superagi_client):
        mock_client_instance = MockClient()
        mock_superagi_client.return_value = mock_client_instance

        mock_client_instance.get_agent_run_status.side_effect = (
            mock_client_instance._get_agent_run_status_side_effect
        )
        mock_client_instance.get_agent_run_resources.side_effect = (
            mock_client_instance._get_agent_run_resources_side_effect
        )
        mock_client_instance.resume_agent.side_effect = (
            mock_client_instance._resume_agent_side_effect
        )

        data1 = {
            "name": "test",
            "email": "test@test.com",
            "phone": "1234567890",
            "message": "message",
            "industry": "Furniture",
            "company_website": "https://www.companywebsite.com",
            "goals": "goals",
            "company_name": "Company Name",
            "superagi_run_complete": False,
            "agent_id": 1,
            "run_id": 1,
        }
        data2 = {
            "name": "test2",
            "email": "test2@test.com",
            "phone": "1234567892",
            "message": "message2",
            "industry": "Electronics",
            "company_website": "https://www.companywebsite2.com",
            "goals": "goals2",
            "company_name": "Company Name 2",
            "superagi_run_complete": False,
            "agent_id": 2,
            "run_id": 2,
        }

        obj1 = ContactLeads.objects.create(**data1)
        obj2 = ContactLeads.objects.create(**data2)

        with self.assertLogs(logger, "INFO") as log_capture:
            handle_workflow_statuses()

        expected_calls_for_status = [
            call(obj1.agent_id, agent_run_filter=AgentRunFilter(run_ids=[obj1.run_id])),
            call(obj2.agent_id, agent_run_filter=AgentRunFilter(run_ids=[obj2.run_id])),
        ]
        mock_client_instance.get_agent_run_status.assert_has_calls(
            expected_calls_for_status, any_order=False
        )

        self.assertFalse(obj1.superagi_run_complete)

        obj1.refresh_from_db()
        mock_client_instance.get_agent_run_resources.assert_called_once_with(
            agent_run_ids=[obj1.run_id]
        )
        self.assertTrue(obj1.superagi_run_complete)
        self.assertEqual(obj1.superagi_resource, "http://test.resource/url.txt")

        mock_client_instance.resume_agent.assert_called_once_with(
            agent_id=obj2.agent_id, agent_run_ids=[obj2.run_id]
        )

        self.assertIn(
            f"INFO:api.utils:Agent run complete for {obj1}", log_capture.output
        )
        self.assertIn(
            f"INFO:api.utils:Resumed agent run for {obj2}", log_capture.output
        )
