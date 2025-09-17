from django import forms
from .models import *

class StudentForm(forms.Form):
    student_id = forms.CharField(max_length=10)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    faculty = forms.ModelChoiceField(
        queryset=Faculty.objects.all(),
        empty_label="Select faculty",
        required=False
    )

    enrolled_sections = forms.ModelMultipleChoiceField(
        queryset=Section.objects.all(),
        required=False,
        widget= forms.CheckboxSelectMultiple
    )

    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea)

