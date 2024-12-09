from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, FormView

from .forms import PostBaseForm, DeletePostForm
from .models import Post
from ..common.forms import CommentForm
from ..common.models import Comment, Like

UserModel = get_user_model()


class PostListView(ListView):
    model = Post
    template_name = 'posts/posts-list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 6

    def get_queryset(self):
        queryset = self.model.objects.all()

        if not self.request.user.has_perm('posts.approve_post'):       # showing only approved posts
            queryset = queryset.filter(approved=True)

        # Search functionality
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(title__icontains=query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pass the list name and search query to the template
        context['query'] = self.request.GET.get('query')
        context['list_name'] = self.model._meta.verbose_name_plural.capitalize()

        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostBaseForm
    template_name = 'posts/create-post.html'
    success_url = reverse_lazy('post-list')

    def form_valid(self, form):
        # Set the logged-in user as the author
        form.instance.author = self.request.user

        # Save the post instance and handle many-to-many fields in the form
        response = super().form_valid(form)

        if self.request.user.has_perm('posts.approve_post'):
            form.instance.approved = True

        # Add a success message
        messages.success(self.request, f"Post '{form.instance.title}' was created successfully.")
        return super().form_valid(form)


class DetailsPostView(DetailView):
    model = Post
    template_name = 'posts/post-details.html'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = self.model.objects.all()

        if not self.request.user.has_perm('posts.approve_post'):
            queryset = queryset.filter(approved=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        context['comments'] = Comment.objects.filter(to_post=post).order_by('-created_at')
        context['comment_form'] = CommentForm()  # Include a comment form
        context['likes_count'] = Like.objects.filter(to_post=post).count()
        context['is_liked'] = Like.objects.filter(to_post=post, user=self.request.user).exists()    # checks if the user is already liked
        context['can_approve'] = self.request.user.has_perm('posts.approve_post')      # checks if the user can approve posts
        context['can_delete_post'] = (
            post.author == self.request.user or
            self.request.user.has_perm('posts.delete_post')
        )
        context['can_delete_comment'] = self.request.user.has_perm('common.delete_comment')

        return context


class EditPostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostBaseForm
    template_name = 'posts/edit-post.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):    # override the test_func method in UserPassesMixin to ensure that only the author can edit.
        post = self.get_object()
        user = self.request.user

        return post.author == user

    def form_valid(self, form):
        post = form.instance

        # If a reader edits the post, set it as unapproved
        if not self.request.user.has_perm('posts.approve_post'):
            post.approved = False

        messages.success(self.request, f"Post '{post.title}' was updated successfully.")

        return super().form_valid(form)


def approve_post(request, pk):
    # Approve the post if the user has permission
    if request.user.has_perm('posts.approve_post'):
        post = get_object_or_404(Post, pk=pk)
        post.approved = True
        post.save()
        messages.success(request, f"Post '{post.title}' was approved.")
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('home')


class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    model = Post
    form_class = DeletePostForm
    template_name = 'posts/delete-post.html'
    success_url = reverse_lazy('post-list')  # Redirect to post list after deletion

    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs['pk'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()
        return context

    def test_func(self):
        post = self.get_object()
        user = self.request.user

        # Allow only the author, redactors, or administrators to delete the post
        return post.author == user or user.has_perm('posts.delete_post')

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()
        messages.success(self.request, f"Post '{post.title}' was deleted successfully!")

        return redirect(self.success_url)

