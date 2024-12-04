from django.urls import path, include
from .views import PlayerListView, PlayerDetailView, PlayerCreateView, PlayerEditView, PlayerDeleteView

urlpatterns = [
    path('', PlayerListView.as_view(), name='player-list'),
    path('<int:pk>/', include([
        path('details/', PlayerDetailView.as_view(), name='player-details'),
        path('edit/', PlayerEditView.as_view(), name='player-edit'),
        path('delete/', PlayerDeleteView.as_view(), name='player-delete')
    ])),
    path('create/', PlayerCreateView.as_view(), name='player-create'),
]