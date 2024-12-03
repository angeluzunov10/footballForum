from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, FormView, DetailView

from footballForum.accounts.forms import AppUserRegisterForm, ProfileEditForm, DeleteProfileForm
from footballForum.accounts.models import Profile

UserModel = get_user_model()


class AppUserRegisterView(CreateView):
    model = UserModel
    form_class = AppUserRegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):     # to keep the user logged in
        response = super().form_valid(form)

        login(self.request, self.object)
        messages.success(self.request, "Registration successful! Welcome!")

        return response


class AppUserLoginView(LoginView):
    template_name = 'accounts/login.html'


class ProfileDetailsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile-details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()

        context['can_delete'] = (
                self.request.user == profile.user or
                self.request.user.has_perm('profiles.delete_profile')
        )
        return context


class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'accounts/profile-delete.html'
    form_class = DeleteProfileForm
    success_url = reverse_lazy('home')

    def get_object(self):
        return get_object_or_404(Profile, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['profile_pk'] = profile.pk
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def test_func(self):
        profile = self.get_object()

        # Allow the profile owner or Administrators to delete
        return (self.request.user == profile.user or
                self.request.user.has_perm('profiles.delete_profile'))

    def form_valid(self, form):
        profile = self.get_object()
        user = profile.user
        user.delete()  # Delete the user and profile
        messages.success(self.request, "The profile was deleted successfully.")
        return super().form_valid(form)


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit.html'

    def get_object(self, queryset=None):
        profile = super().get_object(queryset)

        if self.request.user != profile.user:
            messages.error(self.request, "You are not allowed to edit others' profiles!")
            return redirect('profile-details', pk=self.request.user.pk)
        return profile

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_instance'] = self.request.user     # dynamically passing the logged-in user to the form

        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial['user_instance'] = self.request.user
        return initial

    def get_success_url(self):
        return reverse_lazy(
            'profile-details',
            kwargs={
                'pk': self.object.pk
            }
        )

    def form_valid(self, form):
        messages.success(self.request, f"Your profile was updated successfully!")

        return super().form_valid(form)
