from __future__ import annotations
from typing import TYPE_CHECKING, List

import logging
from .models import ContactLeads

import boto3
from urllib.parse import urlparse

if TYPE_CHECKING:
    from .superagi_integration.agi_services import AGIServices

logger = logging.getLogger(__name__)


def update_completed_runs(
    completed_run_records: List[ContactLeads], services: AGIServices
):
    if len(completed_run_records) < 1:
        return

    for record in completed_run_records:
        try:
            url = services.get_resource_url(record.run_id)
            record.superagi_resource = url
            record.superagi_run_complete = True
            record.save()
            logger.info("Agent run complete for {record}")
        except Exception as e:
            logger.warn(
                f"Exception occured while updating agent run status and resource url for {record}: {str(e)}"
            )


def attempt_resume_agent(paused_run_records: List[ContactLeads], services: AGIServices):
    if len(paused_run_records) < 1:
        return

    for record in paused_run_records:
        try:
            success = services.resume_agent(record.agent_id, record.run_id)
            if not success:
                logger.warn(f"Could not resume agent run for {record}")
            else:
                logger.info(f"Resumed agent run for {record}")
        except Exception as e:
            logger.warn(
                f"Exception occured while resuming agent run for {record}: {str(e)}"
            )


def download_file_from_s3(s3_url, local_path, aws_access_key_id, aws_secret_access_key):
    # Parse the S3 URL to get bucket and key
    parsed_url = urlparse(s3_url)
    bucket = parsed_url.netloc.split(".")[0]
    key = parsed_url.path[1:]

    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    try:
        # Download the file
        s3.download_file(bucket, key, local_path)
        return True
    except Exception as e:
        logger.error(f"Exception occured while downloading file form s3: {str(e)}")
        return False
