from django import forms
from characters.models import FighterClasses


class CharacterCreationForm(forms.Form):
    name = forms.CharField(label='name', max_length=100)
    image = forms.CharField(label='image', max_length=100)
    character_class = forms.ModelChoiceField(
        queryset=FighterClasses.objects.all()
    )


class CharacterRemovalForm(forms.Form):
    removal_check = forms.CharField(
        label='To remove this character, type in "Delete".', max_length=6
    )
