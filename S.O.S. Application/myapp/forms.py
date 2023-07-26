from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from .models import *
from django.forms import modelformset_factory

class CustomUserCreationForm(UserCreationForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists. Please choose a different one.')
        return username


class UserUpdateForm(UserChangeForm):
    password1 = forms.CharField(label='New password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Confirm new password', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        if password1:
            password_validation.validate_password(password2)

        return password2
class LogisticsCompanyForm(forms.ModelForm):
    class Meta:
        model = LogisticsCompany
        fields = ['CompanyName', 'Phone']
class LogisticsCompanyDistrictForm(forms.ModelForm):
    class Meta:
        model = LogisticsCompany_has_District
        fields = ['CostOfOutsource']


class LogisticsCompanyHasDistrictForm(forms.ModelForm):
    class Meta:
        model = LogisticsCompany_has_District
        fields = ['District_DistrictID', 'CostOfOutsource']

    District_DistrictID = forms.ModelChoiceField(queryset=District.objects.all())

class AddLogisticsCompanyForm(forms.ModelForm):
    class Meta:
        model = LogisticsCompany
        fields = ['CompanyID','CompanyName', 'Phone']


class DonatorForm(forms.ModelForm):
    class Meta:
        model = Donator
        fields = ['DonatorID', 'Name', 'Surname', 'Phone']

class DonationCurrencyFormset(forms.ModelForm):
    class Meta:
        model = Donation_has_Currency
        fields = ['Donation_DonationID','Currency_CurrencyType', 'Amount']

class DonationItemFormset(forms.ModelForm):
    class Meta:
        model = Donation_has_Items
        fields = ['Donation_DonationID','Items_ItemID', 'Quantity']
class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['DonationID', 'DonationTime', 'DonationDeliveryTime', 'DonationTime', 'Donator_DonatorID', 'Request_RequestID']