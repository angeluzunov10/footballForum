from django.urls import path, include

from footballForum.posts.views import PostListView, CreatePostView, DetailsPostView, EditPostView, approve_post, \
    DeletePostView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('create/', CreatePostView.as_view(), name='create-post'),
    path('<int:pk>/', include([
        path('details/', DetailsPostView.as_view(), name='post-details'),
        path('edit/', EditPostView.as_view(), name='edit-post'),
        path('approve/', approve_post, name='approve'),
        path('delete/', DeletePostView.as_view(), name='delete-post'),
    ]))
]
