from django import forms
from .models import Drawing

class DrawingForm(forms.ModelForm):
    class Meta:
        model = Drawing
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }
