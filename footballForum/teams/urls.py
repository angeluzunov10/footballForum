from django.urls import path, include
from .views import TeamListView, TeamDetailView, TeamCreateView, TeamEditView, TeamDeleteView

urlpatterns = [
    path('', TeamListView.as_view(), name='team-list'),
    path('<int:pk>/', include([
        path('details/', TeamDetailView.as_view(), name='team-details'),
        path('edit/', TeamEditView.as_view(), name='team-edit'),
        path('delete/', TeamDeleteView.as_view(), name='team-delete')
    ])),
    path('create/', TeamCreateView.as_view(), name='team-create'),
]