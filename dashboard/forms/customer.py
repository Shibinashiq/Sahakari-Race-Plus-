from django import forms
from dashboard.views.imports import *
class CustomerForm(forms.ModelForm):
    # Custom image field with the necessary widget and attributes
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control-file'}),
    )

    batches = forms.ModelMultipleChoiceField(
        queryset=Batch.objects.filter(is_deleted=False, batch_expiry__gte=timezone.now().date()),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = ['image','name', 'email', 'phone_number', 'district', 'batches']  
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'district': forms.Select(attrs={'class': 'form-control', 'required': True}),
        }

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        # Set required fields
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['phone_number'].required = True
        self.fields['district'].required = True
        
        # Set district choices
        self.fields['district'].widget.choices = CustomUser.DISTRICT_CHOICES

        # Handle existing batches for the user
        if self.instance and self.instance.pk:
            subscriptions = Subscription.objects.filter(user=self.instance, is_deleted=False).prefetch_related('batch')
            selected_batches = [batch for subscription in subscriptions for batch in subscription.batch.all()]
            self.fields['batches'].initial = selected_batches

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if CustomUser.objects.exclude(id=self.instance.id).filter(name=name, is_deleted=False).exists():
            raise forms.ValidationError("A user with this name already exists.")
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.exclude(id=self.instance.id).filter(email=email, is_deleted=False).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone_number) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        if CustomUser.objects.exclude(id=self.instance.id if self.instance else None).filter(
            phone_number=phone_number, is_deleted=False
        ).exists():
            raise forms.ValidationError("A user with this phone number already exists.")
        return phone_number

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Handle image upload
        if self.cleaned_data.get('image'):
            instance.image = self.cleaned_data.get('image')

        instance.save()

        selected_batches = self.cleaned_data.get('batches')

        # Handle batch subscriptions
        if selected_batches:
            subscription = Subscription.objects.create(user=instance)
            subscription.batch.add(*selected_batches)

        return instance

    

class SubscriptionCustomerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        customer = kwargs.pop('customer', None)  
        super().__init__(*args, **kwargs)

        if customer:
            subscribed_batches = Subscription.objects.filter(user=customer,is_deleted=False).values_list('batch', flat=True)
            self.fields['batch'].queryset = Batch.objects.filter(is_deleted=False).exclude(id__in=subscribed_batches)
        else:
            self.fields['batch'].queryset = Batch.objects.filter(is_deleted=False)

    batch = forms.ModelChoiceField(
        queryset=Batch.objects.none(), 
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )



