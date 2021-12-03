from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q, Count
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.http import HttpResponseRedirect
from django.views import View
from .models import Post, Comment, UserProfile, Setting
from django.contrib.auth.models import User
from .forms import PostForm, CommentForm
from django.views.generic.edit import UpdateView, DeleteView
import json

from .serializers import UserSerailizer


# Show social feed/explore page to users who are logged in
class PostListView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        #blocked_users = User.objects.filter().blocked_users.users.all()
        posts = Post.objects.filter(author__profile__followers__in=[user.id]).order_by('-date_posted')
        allposts = Post.objects.all().order_by('-date_posted')
        trendingposts = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:10]
        
        comments = Comment.objects.all().order_by('-date_posted')

        form = PostForm()

        context = {
            'post_list': posts,
            'form': form,
            'allposts': allposts,
            'trendingposts': trendingposts,
            'comments': comments,
        }
        return render(request, 'socialmedia\post_list.html', context)
    # Handles post request on the feed (AKA actually creating a post and saving it to the database)
    def post(self, request):
        user = request.user
        posts = Post.objects.filter(author__profile__followers__in=[user.id]).order_by('-date_posted')
        allposts = Post.objects.all().order_by('-date_posted')
        trendingposts = Post.objects.all().order_by('-likes')[:3]
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            messages.success(request, ("Successfully created a post!"))

        context = {
            'post_list': posts,
            'form': form,
            'allposts': allposts,
            'trendingposts': trendingposts,
        }
        return render(request, 'socialmedia\post_list.html', context)

# Explore page for people who aren't logged in
class ExploreView(View):
    def get(self, request):
        posts = Post.objects.all().order_by('-date_posted')
        trending_posts = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:10]
        comments = Comment.objects.all().order_by('-date_posted')

        context = {
            'post_list': posts,
            'trending_posts': trending_posts,
            'comments': comments,
        }
        return render(request, 'socialmedia\explore.html', context)

# This handles the post-detail page, where if you click on a post, it will bring up the comments of that post, etc.
class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        form = CommentForm()

        comments = Comment.objects.filter(post=post).order_by('-date_posted')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }
        return render(request, 'socialmedia\post_detail.html', context)
    
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)
        comments = Comment.objects.filter(post=post).order_by('-date_posted')

        context = {
                    'post': post,
                    'form': form,
                    'comments': comments,
                }

        # create comment
        if request.POST['action'] == 'comment-create':
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.author = request.user
                new_comment.post = post
                new_comment.save()
                messages.success(request, ("You made a comment on", post.author, "'s post!"))

        return render(request, 'socialmedia\post_detail.html', context)

# This handles editting posts.
class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['body']
    template_name = 'socialmedia\post_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Deleting posts
def DeletePost(request, pk):
    post = Post.objects.filter(pk=pk)
    post.delete()
    messages.success(request, ("Post successfully deleted!"))
    return redirect('post-list')

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'socialmedia\post_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Handles deleting comments
def DeleteComment(request, pk):
    comment = Comment.objects.filter(pk=pk)
    comment.delete()
    messages.success(request, ("Comment successfully deleted!"))
    return redirect('post-list')

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'socialmedia\comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# This handles user profiles
class UserProfileView(View):
    def get(self, request, pk):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        blocked_users = User.objects.get(username=request.user).blocked_users.all()
        post = Post.objects.filter(author=user).order_by('-date_posted')
        all_posts = Post.objects.all().order_by('-date_posted')
        liked_posts = Post.objects.filter(likes__in=[user.id]).order_by('-date_posted')
        likes = Post.objects.filter(likes__in=[user.id]).order_by('-date_posted')

        followers = profile.followers.all()
        following = User.objects.filter(followers__in=[user.id])
        if len(followers) == 0:
            is_following = False
            
        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False
        follower_count = len(followers)
        following_count = len(following)
        # check if the profile is in the user's block list
        for blkUser in blocked_users:
            if blkUser == request.user:
                is_blocked = True
                break
        else:
            is_blocked = False

        context = {
            'user' : user,
            'profile' : profile,
            'posts' : post,
            'all_posts' : all_posts,
            'liked_posts' : liked_posts,
            'follower_count' : follower_count,
            'following_count' : following_count,
            'is_following' : is_following,
            'followers' : followers,
            'following' : following,
            'is_blocked' : is_blocked,
            'likes' : likes,
        }

        return render(request, 'socialmedia\profile.html', context)

# Handles editting the user profile
class EditProfileView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    fields = ['name', 'major', 'location', 'hobbies', 'bio', 'birth_date', 'picture']
    template_name = 'socialmedia\profile_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user

# Handles the user settings page
class UserSettingsView(View):
    def get(self, request, pk):
        profile = UserProfile.objects.get(pk=pk)
        user = request.user
        

        context = {
            'user' : user,
            'profile' : profile,
        }
        return render(request, 'socialmedia\\user_settings.html', context)

# Handles follower system
class FollowersView(View):
    def get(self, request, pk):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        followers = profile.followers.all()

        context = {
            'profile': profile,
            'user' : user,
            'followers': followers,
        }

        return render(request, 'socialmedia/followers.html', context)

class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)
        messages.success(request, ("You are now following", profile.user.username))
        return redirect('profile', pk=profile.pk)

class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)
        messages.info(request, ("You have unfollowed", profile.user.username))
        return redirect('profile', pk=profile.pk)

# Search for user profiles
class SearchView(LoginRequiredMixin, View):
    def get(self, request):
        search = self.request.GET.get('search')
        profile_list = UserProfile.objects.filter(
            Q(user__username__icontains=search)
        )
    
        context = {
            'profile_list': profile_list,
            'search': search,
        }

        return render(request, 'socialmedia/search.html', context)

# Likes
class LikePost(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        is_like = False
        fill = "fas"

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like: 
            post.likes.add(request.user)
            messages.success(request, ("You liked",  post.author,  "'s post!"))
        
        if is_like:
            post.likes.remove(request.user)
            messages.success(request, ("You unliked",  post.author,  "'s post!"))
        
        context = {
            'fill': fill,
        }

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next, context)

class LikeComment(LoginRequiredMixin, View):
    def post(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        is_like = False
        fill = "fas"

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like: 
            comment.likes.add(request.user)
        
        if is_like:
            comment.likes.remove(request.user)
        
        context = {
            'fill': fill,
        }

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next, context)

# Change light/dark mode
def userSettings(request):
	user = User.objects.get_or_create(id=1)
	setting = user.setting

	seralizer = UserSerailizer(setting, many=False)

	return JsonResponse(seralizer.data, safe=False)


def updateTheme(request):
	data = json.loads(request.body)
	theme = data['theme']
	
	user = User.objects.get_or_create(id=1)
	user.setting.value = theme
	user.setting.save()
	print('Request:', theme)
	return JsonResponse('Updated..', safe=False)

# Blocking users
class BlockUser(LoginRequiredMixin, View):
    def post(self, request, pk):
        profile = UserProfile.objects.get(pk=pk)
        request.user.blocked_users.add(profile.user)

        return redirect('profile', pk=profile.pk)

class UnblockUser(LoginRequiredMixin, View):
    def post(self, request, pk):
        profile = UserProfile.objects.get(pk=pk)
        request.user.blocked_users.remove(profile.user)

        return redirect('profile', pk=profile.pk)