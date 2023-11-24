from typing import Dict
from django.db import models


class ContactLeads(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=False, null=False)
    message = models.CharField(max_length=300, blank=True, null=True)

    # SuperAGI agent config fields
    company_name = models.CharField(max_length=50, blank=False, null=False)
    company_website = models.URLField(blank=False, null=False)
    industry = models.CharField(max_length=20, blank=False, null=False)
    goals = models.CharField(max_length=200, blank=False, null=False)

    # SuperAGI agent run fields
    superagi_run_complete = models.BooleanField(blank=True, null=True)
    agent_id = models.PositiveIntegerField(blank=True, null=True)
    run_id = models.PositiveIntegerField(blank=True, null=True)
    superagi_resource = models.URLField(blank=True, null=True)

    def get_agi_config_fields(self) -> Dict[str, any]:
        return {
            "company_name": self.company_name,
            "company_website": self.company_website,
            "industry": self.industry,
            "goals": self.goals,
        }

    def __str__(self):
        return f"{self.company_name} agent_id-{self.agent_id} run_id-{self.run_id} run_complete-{self.superagi_run_complete}"

    class Meta:
        app_label = "api"
