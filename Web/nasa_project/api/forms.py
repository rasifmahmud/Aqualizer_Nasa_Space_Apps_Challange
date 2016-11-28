from django import forms
from django.forms import ModelForm
from api.models import UserDevice



class UserDeviceForm(ModelForm):
    class Meta:
        model = UserDevice     
