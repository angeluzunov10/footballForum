from django import forms
from .models import Team


class TeamBaseForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'logo', 'stadium', 'foundation_year']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter team name'}),
            'logo': forms.URLInput(attrs={'placeholder': 'Enter logo URL'}),
            'stadium': forms.TextInput(attrs={'placeholder': 'Enter stadium name'}),
            'foundation_year': forms.NumberInput(attrs={'placeholder': 'Enter foundation year'}),
        }
        labels = {
            'name': 'Team Name:',
            'logo': 'Logo URL:',
            'stadium': 'Stadium:',
            'foundation_year': 'Foundation Year:',
        }
