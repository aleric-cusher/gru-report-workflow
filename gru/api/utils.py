from __future__ import annotations
from typing import TYPE_CHECKING, BinaryIO, List

import logging
import boto3
from urllib.parse import urlparse

from django.core.mail import EmailMessage

if TYPE_CHECKING:
    from .models import ContactLeads
    from .superagi_integration.agi_services import AGIServices

logger = logging.getLogger(__name__)


def update_completed_runs(
    completed_run_records: List[ContactLeads], services: AGIServices
) -> None:
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


def attempt_resume_agent(
    paused_run_records: List[ContactLeads], services: AGIServices
) -> None:
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


def download_file_from_s3(
    s3_url, local_path, aws_access_key_id, aws_secret_access_key
) -> bool:
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


def send_email_with_report(record: ContactLeads, pdf_file: BinaryIO) -> bool:
    email = EmailMessage(
        subject=f"{record.company_name} Analysis Report",
        body=f"Dear {record.name},\n\nYour AI-generated report is ready and attached to this email. If you have any questions or need further assistance, please feel free to reach out. We're here to help!\n\nEnjoy your day!\n\nBest Regards,\nGRU\n",
        from_email="bot@gruworks.com",
        to=[record.email],
    )

    email.attach(
        filename=f"{record.company_name} Report.pdf",
        content=pdf_file.read(),
        mimetype="application/pdf",
    )

    try:
        email.send(fail_silently=False)
        logger.info(
            f"Email with report for {record} sent successfully to {record.email}"
        )
        return False
    except Exception as e:
        logger.error(f"Failed to send email with report to {record}. Error: {str(e)}")
        return True
