from django import forms
from dashboard.models import Batch, Course

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['batch_expiry', 'batch_price', 'course', 'start_date']
        widgets = {
            'batch_expiry': forms.DateInput(attrs={'class': 'form-control', 'required': True, 'type': 'date'}),
            'batch_price': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'course': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'required': True, 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['batch_expiry'].required = True
        self.fields['batch_price'].required = True
        self.fields['course'].required = True
        self.fields['start_date'].required = True

        self.fields['course'].queryset = Course.objects.filter(is_deleted=False)

    def clean_batch_expiry(self):
        batch_expiry = self.cleaned_data.get('batch_expiry')
        if not batch_expiry:
            raise forms.ValidationError("This field is required.")
        return batch_expiry

    def clean_batch_price(self):
        batch_price = self.cleaned_data.get('batch_price')
        if not batch_price:
            raise forms.ValidationError("This field is required.")
        return batch_price

    def clean_course(self):
        course = self.cleaned_data.get('course')
        if not course:
            raise forms.ValidationError("This field is required.")
        return course

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if not start_date:
            raise forms.ValidationError("This field is required.")
        return start_date

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
