from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import TeamBaseForm
from .models import Team


class TeamListView(LoginRequiredMixin, ListView):
    model = Team
    template_name = 'teams/teams-list.html'
    context_object_name = 'teams'
    paginate_by = 10

    def get_queryset(self):
        queryset = self.model.objects.all()
        query = self.request.GET.get('query')

        if query:
            queryset = queryset.filter(name__icontains=query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query')
        context['can_create'] = self.request.user.has_perm('teams.add_team')
        context['can_delete'] = self.request.user.has_perm('teams.delete_team')
        context['list_name'] = self.model._meta.verbose_name_plural.capitalize()  # Add verbose name

        return context


class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    template_name = 'teams/team-details.html'
    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_edit'] = self.request.user.has_perm('teams.change_team')

        return context


class TeamCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Team
    form_class = TeamBaseForm
    template_name = 'teams/create-team.html'
    success_url = reverse_lazy('team-list')

    def test_func(self):
        return self.request.user.has_perm('teams.add_team')


class TeamEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Team
    form_class = TeamBaseForm
    template_name = 'teams/edit-team.html'
    success_url = reverse_lazy('team-list')

    def test_func(self):
        return self.request.user.has_perm('teams.change_team')


class TeamDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Team
    template_name = 'teams/delete-team.html'
    success_url = reverse_lazy('team-list')

    def test_func(self):
        return self.request.user.has_perm('teams.delete_team')
