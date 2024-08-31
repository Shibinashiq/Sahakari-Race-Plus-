from django import forms
from dashboard.models import Lesson
from django.core.exceptions import ValidationError


class LessonForm(forms.ModelForm):
    lesson_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))

    video_title = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    video_url = forms.URLField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    video_is_downloadable = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    video_is_free = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    pdf_title = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    pdf_file = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    pdf_is_downloadable = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    pdf_is_free = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = Lesson
        fields = ['lesson_name', 'image', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lesson_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['video_title'].widget.attrs.update({'class': 'form-control'})
        self.fields['video_url'].widget.attrs.update({'class': 'form-control'})
        self.fields['video_is_downloadable'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['video_is_free'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['pdf_title'].widget.attrs.update({'class': 'form-control'})
        self.fields['pdf_file'].widget.attrs.update({'class': 'form-control'})
        self.fields['pdf_is_downloadable'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['pdf_is_free'].widget.attrs.update({'class': 'form-check-input'})
    def clean(self):
        cleaned_data = super().clean()
        video_url = cleaned_data.get('video_url')
        pdf_file = cleaned_data.get('pdf_file')

        if not video_url and not pdf_file:
            raise ValidationError("Either video URL or PDF file must be provided.")

        return cleaned_data


    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

