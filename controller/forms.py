from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db.models import fields
from controller.models import BillingAddress, Order

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

class BillingAddressForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = ('__all__')
        exclude = ('user',)

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['payment_method',]