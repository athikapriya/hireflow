
from django import forms
from django.forms import ModelForm, DateInput, Textarea, Select, TextInput, NumberInput, FileInput
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import Job, Skill

# =============== job form =============== 
class JobForm(ModelForm):

    skills = forms.CharField(
        widget=TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter skills separated by commas (e.g. Python, Django, React)"
        }),
        required=False
    )

    class Meta:
        model = Job
        fields = [
            "company_name",
            "title",
            "salary",
            "location",
            "employment_type",
            "experience",
            "skills",
            "description",
            "company_logo",
            "deadline",
        ]
        widgets = {
            "company_name": TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter company name"
            }),
            "title": TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter job title"
            }),
            "salary": NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter salary (optional)"
            }),
            "location": TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter job location"
            }),
            "employment_type": Select(attrs={
                "class": "form-select"
            }),
            "experience": Select(attrs={
                "class": "form-select"
            }),
            "description": Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter job description",
                "rows": 3,
            }),
            "company_logo": FileInput(attrs={
                "class": "form-control"
            }),
            "deadline": DateInput(attrs={
                "class": "form-control",
                "type": "date",
                "placeholder": "Select application deadline"
            }),
        }
    
    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        today = timezone.now().date()

        if deadline and deadline < today:
            raise ValidationError("Deadline cannot be in the past.")

        return deadline