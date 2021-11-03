from django.urls import path
from .views import CommentDeleteView, PostListView, PublicPostListView, PostDetailView, PostEditView, PostDeleteView, UserProfileView, EditProfileView, UserSettingsView, AddFollower, RemoveFollower
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('explore', PublicPostListView.as_view(), name='public-post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/edit/<int:pk>/', PostEditView.as_view(), name='post-edit'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', EditProfileView.as_view(), name='profile-edit'),
    path('profile/settings/<int:pk>/', UserSettingsView.as_view(), name='profile-settings'),
    path('profile/<int:pk>/followers/add', AddFollower.as_view(), name='add-follower'),
    path('profile/<int:pk>/followers/remove', RemoveFollower.as_view(), name='remove-follower'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)