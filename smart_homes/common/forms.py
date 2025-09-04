from django import forms
from django.core.exceptions import ValidationError


class ContactForm(forms.Form):
    TYPE_CHOICES = [("home", "Home"), ("business", "Business")]

    name = forms.CharField(max_length=20)
    type = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.RadioSelect)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=10, required=True)
    message = forms.CharField(widget=forms.Textarea, min_length=10)
    plan = forms.FileField(required=False)

    def clean_plan(self):
        uploaded_file = self.cleaned_data.get("plan")
        if not uploaded_file:
            return uploaded_file

        if uploaded_file.content_type != "application/pdf":
            raise ValidationError("Only PDF files are allowed.")

        if uploaded_file.size > 8 * 1024 * 1024:
            raise ValidationError("File too large (max 8MB).")

        return uploaded_file
