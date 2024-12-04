from django import forms
from .models import Player


class PlayerBaseForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'position', 'team', 'player_picture']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter player name'}),
            'position': forms.Select(attrs={'placeholder': 'Enter position'}),
            'team': forms.Select(),
            'player_picture': forms.URLInput(attrs={'placeholder': 'Enter player picture URL'}),
        }
        labels = {
            'name': 'Player Name:',
            'position': 'Position:',
            'team': 'Team:',
            'player_picture': 'Player Picture URL:',
        }