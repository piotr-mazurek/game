from django import forms


class VillageNameChangeForm(forms.Form):
    name = forms.CharField(label='name', max_length=100)
