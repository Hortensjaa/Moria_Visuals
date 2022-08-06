from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Customer


class CustomerCreationForm(UserCreationForm):

    class Meta:
        model = Customer
        fields = ("email",)


class CustomerChangeForm(UserChangeForm):

    class Meta:
        model = Customer
        fields = ("email",)
