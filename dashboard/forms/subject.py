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
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            
        return instance
