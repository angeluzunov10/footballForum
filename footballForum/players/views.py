from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PlayerBaseForm
from .models import Player


class PlayerListView(LoginRequiredMixin, ListView):
    model = Player
    template_name = 'players/player-list.html'
    context_object_name = 'players'
    paginate_by = 10

    def get_queryset(self):     # for the search bar
        queryset = self.model.objects.all()
        query = self.request.GET.get('query')

        if query:
            queryset = queryset.filter(name__icontains=query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query')
        context['can_delete'] = self.request.user.has_perm('players.delete_player')
        context['can_create'] = self.request.user.has_perm('players.add_player')
        context['list_name'] = self.model._meta.verbose_name_plural.capitalize()  # Add verbose name

        return context


class PlayerDetailView(LoginRequiredMixin, DetailView):
    model = Player
    template_name = 'players/player-details.html'
    context_object_name = 'player'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_edit'] = self.request.user.has_perm('players.change_player')

        return context


class PlayerCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = PlayerBaseForm
    model = Player
    template_name = 'players/create-player.html'
    success_url = reverse_lazy('player-list')

    def test_func(self):
        return self.request.user.has_perm('players.add_player')


class PlayerEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Player
    form_class = PlayerBaseForm
    template_name = 'players/edit-player.html'
    success_url = reverse_lazy('player-list')

    def test_func(self):
        return self.request.user.has_perm('players.change_player')


class PlayerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Player
    template_name = 'players/delete-player.html'
    success_url = reverse_lazy('player-list')

    def test_func(self):
        return self.request.user.has_perm('players.delete_player')
