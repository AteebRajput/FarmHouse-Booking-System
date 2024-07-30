from farmhouse.models import Farm, FarmImage, Booking
from django.contrib.auth.models import User
from django import forms
from farmhouse.models import Farm, FarmImage
from .widgets import CustomClearableFileInput


class FarmRegistrationForm(forms.ModelForm):
    images = forms.ImageField(widget=CustomClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Farm
        fields = ['name', 'location', 'contact', 'price_per_night', 'description', 'available_from', 'available_to', 'images']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class BookingForm(forms.ModelForm):
    check_in = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    check_out = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Booking
        fields = ['check_in', 'check_out']
        
class AdminBookingForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="Select User")
    farm = forms.ModelChoiceField(queryset=Farm.objects.all(), label="Select Farm")
    check_in = forms.DateField(widget=forms.SelectDateWidget)
    check_out = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Booking
        fields = ['user', 'farm', 'check_in', 'check_out']


