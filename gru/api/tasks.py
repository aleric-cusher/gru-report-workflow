import logging
from celery import shared_task

from .utils import attempt_resume_agent, update_completed_runs
from .superagi_integration.agent_status import AgentStatus
from .superagi_integration.agi_client_initializer import AGIClientInitializer
from .superagi_integration.agi_services import AGIServices

from .models import ContactLeads

logger = logging.getLogger(__name__)


@shared_task
def add_agent_workflow(model_instance: ContactLeads) -> None:
    data_dict = model_instance.get_agi_config_fields()

    initializer = AGIClientInitializer()
    services = AGIServices(initializer)
    try:
        agent_id, run_id = services.create_and_run_agent(data_dict)
        if run_id and agent_id:
            model_instance.agent_id = agent_id
            model_instance.run_id = run_id
            model_instance.superagi_run_complete = False
            model_instance.save()
    except Exception as e:
        logger.warn(f"Could not add agent workflow: {str(e)}")


@shared_task
def handle_workflow_statuses() -> None:
    incomplete_agent_run_records = ContactLeads.objects.filter(
        superagi_run_complete=False
    )
    if not incomplete_agent_run_records.exists():
        return

    initializer = AGIClientInitializer()
    services = AGIServices(initializer)

    completed_records = []
    paused_records = []

    for record in incomplete_agent_run_records:
        status = services.check_run_status(record.agent_id, record.run_id)
        if status == AgentStatus.COMPLETED:
            completed_records.append(record)
        elif status == AgentStatus.ERROR_PAUSED or status == AgentStatus.PAUSED:
            paused_records.append(record)

    update_completed_runs(completed_records, services)
    attempt_resume_agent(paused_records, services)
