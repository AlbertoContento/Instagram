from django import forms 
from profiles.models import UserProfile

class FollowForm(forms.Form):
    profile_pk = forms.IntegerField(label="Identificador del usuario", widget=forms.HiddenInput())

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'profile_picture',
            'bio',
            'birth_date',
        ]