from copy import copy

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, resolve_url, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DeleteView

from footballForum.common.forms import CommentForm
from footballForum.common.models import Like, Comment
from footballForum.posts.models import Post


# Create your views here.

class HomePageView(TemplateView):
    template_name = 'common/home-page.html'


def likes_functionality(request, post_id):

    post = get_object_or_404(Post, pk=post_id)

    liked_object = Like.objects.filter(
        to_post_id=post_id,
        user=request.user
    ).first()

    if liked_object:
        liked_object.delete()
    else:
        like = Like(to_post=post, user=request.user)
        like.save()

    return redirect(request.META.get('HTTP_REFERER') + f'#{post_id}')


def share_functionality(request, post_id):
    copy(request.META.get('HTTP_HOST') + resolve_url('post-details', post_id))

    return redirect(request.META.get('HTTP_REFERER') + f'#{post_id}')


def comment_functionality(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.to_post = post
            comment.user = request.user
            comment.save()

        return redirect(request.META.get('HTTP_REFERER') + f'#{post_id}')


class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    success_url = reverse_lazy('post-list')

    def test_func(self):
        comment = self.get_object()

        # Readers can delete their own comments
        # Redactors and Administrators can delete any comment
        return comment.user == self.request.user or self.request.user.has_perm('common.delete_comment')

    def get_success_url(self):
        return reverse_lazy('post-details', kwargs={'pk': self.object.to_post.pk})
