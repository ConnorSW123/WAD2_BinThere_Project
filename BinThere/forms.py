from django import forms
from BinThere.models import Location, BinType, Bin, Vote
from django.contrib.auth.models import User
from BinThere.models import UserProfile





class BinForm(forms.ModelForm):
    existing_bin = forms.ModelChoiceField(
        queryset=Bin.objects.all(),
        required=False,  # Allows creating a new bin if left blank
        help_text="Select an existing bin to add bin types, or leave blank to create a new bin."
    )
    
    location_name = forms.CharField(
        max_length=100, required=False, help_text="Enter the name for the new location."
    )
    latitude = forms.DecimalField(
        max_digits=9, decimal_places=6, required=False, help_text="Enter the latitude."
    )
    longitude = forms.DecimalField(
        max_digits=9, decimal_places=6, required=False, help_text="Enter the longitude."
    )
    
    bin_types = forms.ModelMultipleChoiceField(
        queryset=BinType.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple,
        help_text="Select bin types"
    )

    
    overview = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        help_text="Enter a brief overview of the bin."
    )
    
    picture = forms.ImageField(required=False)
    
    class Meta:
        model = Bin
        fields = (
            'existing_bin', 'location_name', 'latitude', 'longitude', 'bin_types', 'picture'
        )

    def clean(self):
        """
        Ensure that either an existing bin is selected OR a new bin's location data is provided.
        """
        cleaned_data = super().clean()
        existing_bin = cleaned_data.get("existing_bin")
        location_name = cleaned_data.get("location_name")
        latitude = cleaned_data.get("latitude")
        longitude = cleaned_data.get("longitude")

        if existing_bin and (location_name or latitude or longitude):
            raise forms.ValidationError(
                "You cannot select an existing bin and provide a new location at the same time."
            )

        if not existing_bin and (not location_name or latitude is None or longitude is None):
            raise forms.ValidationError(
                "To create a new bin, you must provide a location name, latitude, and longitude."
            )

        return cleaned_data








class BinTypeForm(forms.Form):
    bin_type = forms.ModelChoiceField(queryset=BinType.objects.all(), empty_label="Select a Bin Type")






class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)