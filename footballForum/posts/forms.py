from django import forms
from footballForum.players.models import Player
from footballForum.posts.models import Post
from footballForum.teams.models import Team


class PostBaseForm(forms.ModelForm):
    player_names = forms.CharField(
        required=False,
        widget=forms.TextInput(),
        help_text='Enter player names, included in post, separated by commas',
        label='Tagged players:'
    )

    team_names = forms.CharField(
        required=False,
        widget=forms.TextInput(),
        help_text='Enter team names, included in post, separated by commas',
        label='Tagged teams:'
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter the post title...'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter the post content...'}),
            'image': forms.URLInput(attrs={'placeholder': 'Enter the image URL...'}),
        }
        labels = {
            'title': 'Title:',
            'content': 'Content:',
            'image': 'Image URL:',
            'tagged_players': 'Tags:'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # If editing an existing post
            self.fields['player_names'].initial = ', '.join(
                player.name for player in self.instance.tagged_players.all()
            )
            self.fields['team_names'].initial = ', '.join(
                team.name for team in self.instance.tagged_teams.all()
            )

    def save(self, commit=True):
        post = super().save(commit=False)

        if commit:
            post.save()

        # Handle tagged players
        player_names = self.cleaned_data.get('player_names', '')

        if player_names:
            player_names = [name.strip() for name in player_names.split(',') if name.strip()]
            player_names = list(set(player_names))  # Remove duplicates
            for name in player_names:
                player, _ = Player.objects.get_or_create(name=name)
                post.tagged_players.add(player)

        # Handle tagged teams
        team_names = self.cleaned_data.get('team_names', '')

        if team_names:
            post.tagged_teams.clear()  # Clear existing teams to avoid duplication
            team_names = [name.strip() for name in team_names.split(',') if name.strip()]
            team_names = list(set(team_names))  # Remove duplicates
            for name in team_names:
                team, _ = Team.objects.get_or_create(name=name)
                post.tagged_teams.add(team)

        return post


class DeletePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'readonly': True}),
            'content': forms.Textarea(attrs={'readonly': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['readonly'] = True
            field.widget.attrs['disabled'] = True
