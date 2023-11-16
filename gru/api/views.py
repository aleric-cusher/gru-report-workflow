import json
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render

from .forms import ContactLeadsForm


def contact_lead(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Method Not Allowed. Allowed methods are: POST"}, status=405
        )

    form_data = json.loads(request.body)
    bound_form = ContactLeadsForm(form_data)

    if bound_form.is_valid():
        bound_form.save()
        return JsonResponse(
            {
                "success": True,
                "message": "Form recieved, We will get back to you shortly!",
            },
            status=200,
        )

    errors = {field: bound_form.errors[field][0] for field in bound_form.errors}
    return JsonResponse({"success": False, "error": errors}, status=400)
