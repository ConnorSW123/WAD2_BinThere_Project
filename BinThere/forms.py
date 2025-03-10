from django import forms
from BinThere.models import Location, BinType, Bin, Vote
from django.contrib.auth.models import User
from BinThere.models import UserProfile



class BinForm(forms.ModelForm):
    # Fields for adding a new bin
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        required=False,  # This will allow the user to leave this field blank if they want to add a new location
        help_text="Select the location for the bin, or leave it blank to create a new location."
    )
    bin_type = forms.ModelChoiceField(
        queryset=BinType.objects.all(),
        help_text="Select the type of the bin."
    )
    latitude = forms.DecimalField(
        max_digits=9, decimal_places=6, required=False,  # Will be used only if a new location is created
        help_text="Enter the latitude of the new location."
    )
    longitude = forms.DecimalField(
        max_digits=9, decimal_places=6, required=False,  # Will be used only if a new location is created
        help_text="Enter the longitude of the new location."
    )
    location_name = forms.CharField(
        max_length=100, required=False,  # Only required if a new location is being created
        help_text="Enter the name for the new location."
    )
    upvotes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    downvotes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Bin
        fields = ('location', 'bin_type', 'latitude', 'longitude', 'location_name', 'upvotes', 'downvotes')  # added location_name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # No need to set added_by field in the form itself



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)