from django import forms
from dashboard.models import Subject ,Course

class SubjectForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(is_deleted=False),
        widget=forms.Select(attrs={'class': 'form-control', 'required': True}),
        empty_label="Select a Course"
    )
   
    class Meta:
        model = Subject
        fields = ['subject_name', 'image', 'description' , 'course']
        widgets = {
                'subject_name': forms.TextInput(
                    attrs={'class': 'form-control', 'placeholder': 'Enter subject name'}
                ),
                'image': forms.FileInput(attrs={'class': 'form-control', 'type': 'file'}),
                'description': forms.Textarea(
                    attrs={'class': 'form-control', 'rows': 4, 'cols': 40, 'placeholder': 'Enter a brief description'}
                ),
            }
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            
        return instance
