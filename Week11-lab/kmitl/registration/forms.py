from django import forms
from .models import *
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.forms.widgets import *
from django.forms.fields import SplitDateTimeField

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = "__all__"


    
class StudentProfileForm(ModelForm):
    class Meta:
        model = StudentProfile
        # fields = "__all__"
        exclude = ["student"]
        widgets = {
            "image": FileInput(attrs={"class":"hidden"})
        }
    def clean_email(self):
        cleaned_data = self.clean()
        email = cleaned_data.get("email")
        if not email.endswith("@kmitl.ac.th"):
            return False
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
