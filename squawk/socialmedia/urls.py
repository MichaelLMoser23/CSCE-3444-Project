from django.urls import path
from .views import CommentDeleteView, DeleteComment, DeletePost, BlockUser, UnblockUser ,PostListView, LikeComment, ExploreView, LikePost, SearchView, FollowersView, PostDetailView, PostEditView, PostDeleteView, UserProfileView, EditProfileView, UserSettingsView, AddFollower, RemoveFollower
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('explore/', ExploreView.as_view(), name='explore'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/edit/<int:pk>/', PostEditView.as_view(), name='post-edit'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/delete/', DeletePost, name='delete-post'),
    path('post/<int:pk>/like', LikePost.as_view(), name='like'),
    path('post/<int:post_pk>/comment/<int:pk>/like', LikeComment.as_view(), name='comment-like'),
    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('post/<int:pk>/comment/delete/', DeleteComment, name='delete-comment'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', EditProfileView.as_view(), name='profile-edit'),
    path('profile/settings/<int:pk>/', UserSettingsView.as_view(), name='profile-settings'),
    path('profile/<int:pk>/followers', FollowersView.as_view(), name='followers'),
    path('profile/<int:pk>/followers/add', AddFollower.as_view(), name='add-follower'),
    path('profile/<int:pk>/followers/remove', RemoveFollower.as_view(), name='remove-follower'),
    path('profile/<int:pk>/blocked_user/add', BlockUser.as_view(), name='block-user'),
    path('profile/<int:pk>/blocked_user/remove', UnblockUser.as_view(), name='unblock-user'),
    path('search/', SearchView.as_view(), name='search'),
    path('user_settings/', views.userSettings, name="user_settings"),
    path('update_theme/', views.updateTheme, name="update_theme"),
    
]

