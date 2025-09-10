import datetime
from django import forms


DEPARTMENT_CHOICES = (
    ("it", "IT"),
    ("hr", "Human resource"),
    ("fi", "Finance"),
    ("ac", "Accounting"),
)

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
    issue_date = forms.DateField(widget=forms.SelectDateWidget(
        years=range(datetime.date.today().year - 5, datetime.date.today().year + 1))
    )
    department = forms.ChoiceField(
        choices=DEPARTMENT_CHOICES,  
        label='Responsible department',
        widget=forms.RadioSelect
    )