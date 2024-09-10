from django import forms
from dashboard.views.imports import *
from dashboard.models import *
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

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        batch_expiry = cleaned_data.get('batch_expiry')

        if start_date and batch_expiry:
            if start_date > batch_expiry:
                raise forms.ValidationError({
                    self.add_error('batch_expiry', 'The expiry date cannot be earlier than the start date.')
                })
            if start_date == batch_expiry:
                raise forms.ValidationError({
                    self.add_error('batch_expiry', 'The expiry date cannot be equals the start date.')
                })

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance



class BatchCustomerForm(forms.ModelForm):
    

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'phone_number', 'district',]
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

        if self.instance and self.instance.pk:
            subscriptions = Subscription.objects.filter(user=self.instance, is_deleted=False).prefetch_related('batch')
            selected_batches = [batch for subscription in subscriptions for batch in subscription.batch.all()]
            self.fields['batches'].initial = selected_batches

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if CustomUser.objects.exclude(id=self.instance.id).filter(name=name,is_deleted=False).exists():
            raise forms.ValidationError("A user with this name already exists.")
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.exclude(id=self.instance.id).filter(email=email,is_deleted=False).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if CustomUser.objects.exclude(id=self.instance.id).filter(phone_number=phone_number,is_deleted=False).exists():
            raise forms.ValidationError("A user with this phone number already exists.")
        return phone_number

   