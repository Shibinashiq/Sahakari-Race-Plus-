from django import forms
from dashboard.models import Subject ,Course ,TalentHuntSubject

class TalentHuntSubjectForm(forms.ModelForm):
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.none(),  
        widget=forms.Select(attrs={'class': 'form-control', 'required': True}),
        empty_label="Select a subject"
    )

    class Meta:
        model = TalentHuntSubject
        fields = ['title', 'subject']
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter title'}
            ),
        }

    def __init__(self, *args, **kwargs):
        course = kwargs.pop('course', None)  
        super().__init__(*args, **kwargs)
        if course:
            self.fields['subject'].queryset = Subject.objects.filter(course=course, is_deleted=False)
