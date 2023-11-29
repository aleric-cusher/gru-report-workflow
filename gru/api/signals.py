from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .tasks import add_agent_workflow, process_and_email_report
from .models import ContactLeads


@receiver(post_save, sender=ContactLeads)
def on_contact_lead_save(
    sender: ContactLeads, instance: ContactLeads, created: bool, **kwargs
):
    if created:
        add_agent_workflow.delay(instance.pk)


@receiver(pre_save, sender=ContactLeads)
def on_superagi_run_complete_update(
    sender: ContactLeads, instance: ContactLeads, **kwargs
):
    if instance.pk is not None and ContactLeads.objects.filter(pk=instance.pk).exists():
        snapshot = ContactLeads.objects.get(pk=instance.pk)
        if (
            (not snapshot.superagi_run_complete)
            and instance.superagi_run_complete
            and instance.superagi_resource
        ):
            process_and_email_report.delay(instance.pk)
