from django import forms

from footballForum.common.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Add a comment...',
                'rows': 4,
            }),
        }
        labels = {
            'content': 'Comment:',
        }