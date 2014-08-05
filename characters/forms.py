from django import forms
from characters.models import FighterClasses, Character

class CharacterCreationForm(forms.Form):
    name = forms.CharField(label='name', max_length=100)
    image = forms.CharField(label='image', max_length=100)
    character_class = forms.ModelChoiceField(queryset = FighterClasses.objects.all())