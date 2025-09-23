from django.forms import ModelForm, TimeInput, TimeField, modelformset_factory, ValidationError, BaseModelFormSet, FileInput
from registration.models import *

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = "__all__"

class StudentProfileForm(ModelForm):
    class Meta:
        model = StudentProfile
        exclude = ['student']

        widgets = {
            "image": FileInput(attrs={"class": "hidden"})
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if email and not email.endswith("@kmitl.ac.th"):
            raise ValidationError("Email must end with `@kmitl.ac.th`")
        return cleaned_data

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = "__all__"

class SectionForm(ModelForm):
    start_time = TimeField(widget=TimeInput(attrs={"class": "input", "type": "time"}))
    end_time = TimeField(widget=TimeInput(attrs={"class": "input", "type": "time"}))
    class Meta:
        model = Section
        exclude = ['course']

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        capacity = cleaned_data.get('capacity')
        if (end_time < start_time):
            self.add_error(None, "end_time must be greater than start_time")
        if (not capacity > 20):
            self.add_error(None, "capacity must be greater than 20")
        return cleaned_data

SectionFormSet = modelformset_factory(Section, form=SectionForm, can_delete=True)