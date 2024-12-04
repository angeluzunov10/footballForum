from django.urls import path, include

from footballForum.common.views import HomePageView, likes_functionality, share_functionality, comment_functionality, \
    DeleteCommentView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('like/<int:post_id>/', likes_functionality, name='like'),
    path('comment/', include([
        path('<int:post_id>/', comment_functionality, name='comment'),
        path('<int:pk>/delete/', DeleteCommentView.as_view(), name='delete-comment')
    ])),
    path('share/<int:post_id>/', share_functionality, name='share'),
]
