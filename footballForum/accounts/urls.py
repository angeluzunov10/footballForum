from django.contrib.auth.views import LogoutView
from django.urls import path, include
from .views import AppUserRegisterView, AppUserLoginView, ProfileEditView, ProfileDeleteView, ProfileDetailsView

urlpatterns = [
    path('register/', AppUserRegisterView.as_view(), name='register'),
    path('login/', AppUserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', include([
        path('details/', ProfileDetailsView.as_view(), name='profile-details'),
        path('delete/', ProfileDeleteView.as_view(), name='profile-delete'),
        path('edit/', ProfileEditView.as_view(), name='profile-edit'),
        ])),
]
