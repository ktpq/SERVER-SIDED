from django import forms
from .models import *
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.forms.widgets import *
from django.forms.fields import SplitDateTimeField

# class StudentForm(forms.Form):
#     student_id = forms.CharField(max_length=10)
#     first_name = forms.CharField(max_length=100)
#     last_name = forms.CharField(max_length=100)

#     faculty = forms.ModelChoiceField(
#         queryset=Faculty.objects.all(),
#         empty_label="Select faculty",
#         required=False
#     )

#     enrolled_sections = forms.ModelMultipleChoiceField(
#         queryset=Section.objects.all(),
#         required=False,
#         widget= forms.CheckboxSelectMultiple
#     )

#     email = forms.EmailField()
#     phone_number = forms.CharField(max_length=20)
#     address = forms.CharField(widget=forms.Textarea)

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = "__all__"


    
class StudentProfileForm(ModelForm):
    class Meta:
        model = StudentProfile
        # fields = "__all__"
        exclude = ["student"]
    def clean_email(self):
        cleaned_data = self.clean()
        email = cleaned_data.get("email")
        if not email.endswith("@kmitl.ac.th"):
            raise ValidationError("Email must end with @kmitl.ac.th")
        return email
    
class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = "__all__"

class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = "__all__"
        exclude = ["course"]
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    

    def clean(self):
        clean_data = super().clean()
        start_time = clean_data.get("start_time")
        end_time = clean_data.get("end_time")
        capacity = clean_data.get("capacity")

        if start_time and end_time and end_time < start_time:
            self.add_error("end_time", "End time must be after start time")
        if capacity is not None and capacity <= 20:
            self.add_error("capacity", "Capacity must be over 20")
        return clean_data
