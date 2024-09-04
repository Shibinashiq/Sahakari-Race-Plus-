from django import forms
from dashboard.models import Exam, Subject,Question
from ckeditor_uploader.widgets import CKEditorUploadingWidget
class ExamForm(forms.ModelForm):
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    duration = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'})
    )
    
    class Meta:
        model = Exam
        fields = ['title', 'subject', 'duration']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter exam title'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, commit=True):    
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance




class QuestionForm(forms.ModelForm):
    # question_description = forms.CharField(widget=CKEditorUploadingWidget())
    question_description = forms.CharField(widget=CKEditorUploadingWidget())
    hint = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Question
        fields = [
            'question_type',
            'question_description',
            'hint',
            'options',
            'right_answers',
        ]
        widgets = {
            'question_type': forms.Select(attrs={'class': 'form-control'}),
            'question_description': forms.Textarea(attrs={'class': 'form-control', 'id': 'editor1'}),
            'hint': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter hint'}),
            'options': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter options separated by commas'}),
            'right_answers': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter right answers separated by commas'}),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['question_description'].initial = self.fields['question_description'].initial or ''
            self.fields['hint'].initial = self.fields['hint'].initial or ''