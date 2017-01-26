from django import forms

from .models import Imageskin


class ImageskinForm(forms.ModelForm):
    class Meta:
        model = Imageskin
        fields = ('docfile', 'name', 'disease', 'sourcedata',)
