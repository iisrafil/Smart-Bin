from django import forms

from api.models import Device, AppUser


class DeviceAddForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['id', 'name', 'location', 'dustbinHeight']


class DeviceUpdateForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['user', 'id', 'name', 'location', 'dustbinHeight']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ['status']

