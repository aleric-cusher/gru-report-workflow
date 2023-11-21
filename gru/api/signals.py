from django.db.models.signals import post_save
from django.dispatch import receiver

from .tasks import add_agent_workflow
from .models import ContactLeads


@receiver(post_save, sender=ContactLeads)
def on_contact_lead_save(sender, instance, created, **kwargs):
    if created:
        add_agent_workflow.delay(instance)
