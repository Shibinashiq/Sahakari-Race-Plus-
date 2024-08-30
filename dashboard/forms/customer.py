from django import forms
from dashboard.models import CustomUser
class CustomerForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'phone_number', 'district']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'district': forms.Select(attrs={'class': 'form-control', 'required': True}),
        }

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['phone_number'].required = True
        self.fields['district'].required = True
        self.fields['district'].widget.choices = CustomUser.DISTRICT_CHOICES

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if CustomUser.objects.exclude(id=self.instance.id).filter(name=name).exists():
            raise forms.ValidationError("A user with this name already exists.")
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.exclude(id=self.instance.id).filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if CustomUser.objects.exclude(id=self.instance.id).filter(phone_number=phone_number).exists():
            raise forms.ValidationError("A user with this phone number already exists.")
        return phone_number

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance