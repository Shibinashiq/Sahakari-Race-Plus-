from django import forms
from django.core.exceptions import ValidationError
from dashboard.models import Course ,Batch
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

class AddForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'image', 'description']
        widgets = {
            'course_name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'type': 'file'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 40}),
        }
        error_messages = {
            'course_name': {
                'required': "Course name is required.",
            },
            'image': {
                'required': "An image is required.",
            },
            'description': {
                'required': "A description is required.",
            },
        }

    def __init__(self, *args, **kwargs):
        super(AddForm, self).__init__(*args, **kwargs)
        self.fields['course_name'].required = True
        self.fields['image'].required = True
        self.fields['description'].required = True

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance