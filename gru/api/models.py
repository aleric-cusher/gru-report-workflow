from django.db import models


class ContactLeads(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15)
    message = models.CharField(max_length=300, blank=True, null=True)

    # SuperAGI agent config fields
    company_name = models.CharField(max_length=50)
    company_website = models.URLField()
    industry = models.CharField(max_length=20)
    goals = models.CharField(max_length=200)

    # SuperAGI agent run fields
    superagi_run_complete = models.BooleanField(blank=True, default=False)
    agent_id = models.PositiveIntegerField(blank=True, null=True)
    run_id = models.PositiveIntegerField(blank=True, null=True)
