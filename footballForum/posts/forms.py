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
        if self.instance.pk:  # prefilling the teams and players if edit an existing post
            self.fields['player_names'].initial = ', '.join(
                player.name for player in self.instance.tagged_players.all()
            )
            self.fields['team_names'].initial = ', '.join(
                team.name for team in self.instance.tagged_teams.all()
            )

    def handle_tagging(self, tag_field_name, model, relation_field, post_instance):
        tag_names = self.cleaned_data.get(tag_field_name, '')

        if not tag_names:  # If the field is empty, clear the related field
            getattr(post_instance, relation_field).clear()
            return

        tag_names = [name.strip() for name in tag_names.split(',') if name.strip()]
        unique_tag_names = list(set(tag_names))  # Remove duplicates in input

        # Fetch existing tags and add only non-existing ones
        tags_to_set = []
        for name in unique_tag_names:
            tag, _ = model.objects.get_or_create(name=name)
            tags_to_set.append(tag)

        # Replace existing tags with the new list of tags
        getattr(post_instance, relation_field).set(tags_to_set)

    def save(self, commit=True):
        post = super().save(commit=False)

        if commit:
            post.save()

        # Handle tagged players
        self.handle_tagging('player_names', Player, 'tagged_players', post)

        # Handle tagged teams
        self.handle_tagging('team_names', Team, 'tagged_teams', post)

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
