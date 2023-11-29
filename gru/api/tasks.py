import json
import logging
from celery import shared_task

from .utils import (
    attempt_resume_agent,
    generate_pdf,
    read_file_from_s3,
    send_email_with_report,
    update_completed_runs,
)
from .superagi_integration.agent_status import AgentStatus
from .superagi_integration.agi_client_initializer import AGIClientInitializer
from .superagi_integration.agi_services import AGIServices

from .models import ContactLeads

logger = logging.getLogger(__name__)


@shared_task
def add_agent_workflow(primary_key: int) -> None:
    model_instance = ContactLeads.objects.get(pk=primary_key)
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
        logger.error(f"Could not add agent workflow for {model_instance}: {str(e)}")


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


@shared_task
def process_and_email_report(primary_key: int) -> bool:
    record = ContactLeads.objects.get(pk=primary_key)
    file_content = read_file_from_s3(record.superagi_resource)

    if file_content is None:
        return False

    data = json.loads(file_content)
    pdf_file = generate_pdf(data)

    success = send_email_with_report(record, pdf_file)
    if success:
        record.email_sent = True
        record.save()

    return success
