from django import forms
from dashboard.models import Chapter ,Subject

class ChapterForm(forms.ModelForm):
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.filter(is_deleted=False),
        widget=forms.Select(attrs={'class': 'form-control', 'required': True}),
        empty_label="Select a subject",
    )
   
    class Meta:
        model = Chapter
        fields = ['chapter_name', 'image', 'description' ,'subject']
        widgets = {
            'chapter_name':  forms.TextInput(
                    attrs={'class': 'form-control', 'placeholder': 'Enter chapter name'}
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


