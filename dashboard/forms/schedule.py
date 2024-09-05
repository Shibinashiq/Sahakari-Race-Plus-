from django import forms
from dashboard.models import Chapter,Lesson , Schedule ,Exam
from django.core.exceptions import ValidationError

class ScheduleForm(forms.ModelForm):
    lesson = forms.ModelChoiceField(
        queryset=Lesson.objects.filter(is_deleted=False),
        widget=forms.Select(attrs={'class': 'form-control', 'required': True}),
        empty_label="Select a lesson",
    )
    exam = forms.ModelChoiceField(
        queryset=Exam.objects.filter(is_deleted=False),
        widget=forms.Select(attrs={'class': 'form-control', 'required': True}),
        empty_label="Select an exam",
    )

    class Meta:
        model = Schedule
        fields = ['title', 'lesson', 'exam', 'date']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Enter date'}),
        }
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            
        return instance
