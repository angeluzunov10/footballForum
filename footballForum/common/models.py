from django.contrib.auth import get_user_model
from django.db import models
from footballForum.posts.models import Post

# Create your models here.


UserModel = get_user_model()


class Like(models.Model):
    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        related_name='likes',
    )

    to_post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='likes',
    )

    def __str__(self):
        return f'{self.user} liked {self.to_post}'


class Comment(models.Model):
    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    to_post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}: {self.content[:20]}'
