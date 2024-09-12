from django import forms
from dashboard.views.imports import *
class CustomerForm(forms.ModelForm):
    batches = forms.ModelMultipleChoiceField(
        queryset=Batch.objects.filter(is_deleted=False, batch_expiry__gte=timezone.now().date()),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'phone_number', 'district', 'batches']
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

    def save(self, commit=True):
        instance = super().save(commit=False)  

        instance.save()  

        selected_batches = self.cleaned_data.get('batches')

        # Subscription.objects.filter(user=instance).delete()

        if selected_batches:
            subscription = Subscription.objects.create(user=instance) 
            subscription.batch.add(*selected_batches)  

        return instance
    

from django import forms

class SubscriptionCustomerForm(forms.Form):
    batch = forms.ModelChoiceField(
        queryset=Batch.objects.filter(is_deleted=False),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # No need to redefine queryset again here if it's already done in field declaration
    def save(self, commit=True):
        # Since this is a non-ModelForm form, 'super().save' doesn't apply
        # You'll need to manage the saving logic depending on your use case
        batch = self.cleaned_data.get('batch')
        
        # Handle instance saving or return
        if commit:
            # Perform any save logic, if necessary, related to 'batch'
            pass
        return batch
