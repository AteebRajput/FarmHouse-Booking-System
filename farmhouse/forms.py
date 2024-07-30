# farmhouse/forms.py
from django import forms
from .models import Farm, FarmImage, Booking

class FarmRegistrationForm(forms.ModelForm):
    available_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    available_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    images = forms.ImageField(widget=forms.ClearableFileInput(), required=False)

    class Meta:
        model = Farm
        fields = ['name', 'location', 'description', 'contact', 'price_per_night', 'available_from', 'available_to']

class FarmImageForm(forms.ModelForm):
    class Meta:
        model = FarmImage
        fields = ['image']

class BookingForm(forms.ModelForm):
    check_in = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    check_out = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Booking
        fields = ['check_in', 'check_out']



class FarmSearchForm(forms.Form):
    location = forms.ChoiceField(choices=[], required=False, label="Location")
    farm_name = forms.CharField(max_length=100, required=False, label="Farm Name")

    def __init__(self, *args, **kwargs):
        super(FarmSearchForm, self).__init__(*args, **kwargs)
        locations = Farm.objects.values_list('location', flat=True).distinct()
        self.fields['location'].choices = [(location, location) for location in locations]

