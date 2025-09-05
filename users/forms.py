
# Music upload form
from django import forms
from .models import MusicTrack

class MusicTrackUploadForm(forms.ModelForm):
    class Meta:
        model = MusicTrack
        fields = ['title', 'artist', 'album', 'genre', 'audio_file', 'cover_image']
from django.contrib.auth.models import User

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['mobile_number']
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    USER_TYPE_CHOICES = [
        ('normal', 'Normal'),
        ('kid', 'Kid'),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect, initial='normal', label='Account Type')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User  # If adding more profile fields, change to a Profile model
        fields = ['password']  # User can reset password
