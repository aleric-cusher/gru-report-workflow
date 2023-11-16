from django.shortcuts import redirect
from django.urls import path
from . import views

urlpatterns = [
    path("contact-lead/", views.contact_lead, name="contact-lead"),
]
