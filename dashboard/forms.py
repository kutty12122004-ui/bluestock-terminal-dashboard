# dashboard/forms.py
from django import forms

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        label="Select Company CSV File",
        widget=forms.FileInput(attrs={'accept': '.csv', 'class': 'form-control'})
    )