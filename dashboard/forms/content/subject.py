from django import forms
from dashboard.models import Subject

class SubjectForm(forms.ModelForm):
   
    class Meta:
        model = Subject
        fields = ['subject_name', 'image', 'description']
        widgets = {
            'subject_name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'type': 'file'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 40}),
        }

    def clean(self):
        cleaned_data = super().clean()

        subject_name = cleaned_data.get('subject_name')
        image = cleaned_data.get('image')

        if not subject_name or len(subject_name) < 3:
            self.add_error('subject_name', 'Subject name must be at least 3 characters long.')

        if not image:
            self.add_error('image', 'Please upload an image.')

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        if not self.cleaned_data.get('description'):
            self.add_error('description', 'Description cannot be empty.')

        if not self.errors and commit:
            instance.save()

        return instance