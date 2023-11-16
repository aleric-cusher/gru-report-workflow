from django import forms
from .models import ContactLeads


class ContactLeadsForm(forms.ModelForm):
    class Meta:
        model = ContactLeads
        fields = [
            "name",
            "email",
            "phone",
            "message",
            "company_name",
            "company_website",
            "industry",
            "goals",
        ]

    def __init__(self, *args, **kwargs):
        super(ContactLeadsForm, self).__init__(*args, **kwargs)

        self.fields["email"].required = False
        self.fields["message"].required = False
        self.fields["company_website"].required = True
