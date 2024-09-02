from django import forms
from dashboard.models import Question, Exam

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'question_type',
            'question_description',
            'hint',
            'options',
            'right_answers',
            'exam'
        ]
        widgets = {
            'question_description': forms.Textarea(attrs={'class': 'form-control', 'id': 'editor1'}),
            'hint': forms.Textarea(attrs={'class': 'form-control'}),
            'options': forms.Textarea(attrs={'class': 'form-control'}),
            'right_answers': forms.Textarea(attrs={'class': 'form-control'}),
            'exam': forms.Select(attrs={'class': 'form-control'})
        }