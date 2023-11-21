import logging
from celery import shared_task

from .superagi_integration.agi_client_initializer import AGIClientInitializer
from .superagi_integration.agi_services import AGIServices

from .models import ContactLeads

logger = logging.getLogger(__name__)


@shared_task
def add_agent_workflow(model_instance: ContactLeads):
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
