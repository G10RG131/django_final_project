from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import MyUser
from .models import Car


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'brand', 'model', 'year', 'rental_price_per_day', 'size',
            'transmission', 'phone_number', 'city', 'fuel_capacity',
            'picture1', 'picture2', 'picture3'
        ]


class PhoneAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Phone Number')


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ['phone', 'email', 'name', 'surname', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password and Confirm Password do not match")
