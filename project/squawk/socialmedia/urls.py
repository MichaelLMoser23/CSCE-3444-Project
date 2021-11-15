from django.urls import path
from .views import CommentDeleteView, PostListView, ExploreView, LikePost, SearchView, FollowersView, PostDetailView, PostEditView, PostDeleteView, UserProfileView, EditProfileView, UserSettingsView, AddFollower, RemoveFollower
from django.conf.urls.static import static

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('explore/', ExploreView.as_view(), name='explore'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/edit/<int:pk>/', PostEditView.as_view(), name='post-edit'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/like', LikePost.as_view(), name='like'),
    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', EditProfileView.as_view(), name='profile-edit'),
    path('profile/settings/<int:pk>/', UserSettingsView.as_view(), name='profile-settings'),
    path('profile/<int:pk>/followers', FollowersView.as_view(), name='followers'),
    path('profile/<int:pk>/followers/add', AddFollower.as_view(), name='add-follower'),
    path('profile/<int:pk>/followers/remove', RemoveFollower.as_view(), name='remove-follower'),
    path('search/', SearchView.as_view(), name='search'),
    
]

