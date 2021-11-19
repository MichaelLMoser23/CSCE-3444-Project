from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
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


# Create your views here.
class PostListView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
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

        context = {
            'post_list': posts,
            'form': form,
            'allposts': allposts,
            'trendingposts': trendingposts,
        }
        return render(request, 'socialmedia\post_list.html', context)

# Explore page
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

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

        comments = Comment.objects.filter(post=post).order_by('-date_posted')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }
        return render(request, 'socialmedia\post_detail.html', context)

class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['body', 'image']
    template_name = 'socialmedia\post_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
        
def Delete_Post(request, pk):
    post = Post.objects.filter(pk=pk)
    post.delete()
    return redirect('post-list')

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'socialmedia\post_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
        

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'socialmedia\comment_delete.html'
    
    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class UserProfileView(View):
    def get(self, request, pk):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        post = Post.objects.filter(author=user).order_by('-date_posted')

        followers = profile.followers.all()
        if len(followers) == 0:
            is_following = False
            
        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False

        follower_count = len(followers)

        context = {
            'user' : user,
            'profile' : profile,
            'posts' : post,
            'follower_count' : follower_count,
            'is_following' : is_following,
            'followers' : followers,
        }

        return render(request, 'socialmedia\profile.html', context)

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

class UserSettingsView(View):
    def get(self, request, pk):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        

        context = {
            'user' : user,
            'profile' : profile,
        }
        return render(request, 'socialmedia\\user_settings.html', context)

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

        return redirect('profile', pk=profile.pk)

class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)

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
        
        if is_like:
            post.likes.remove(request.user)
        
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
	user, created = User.objects.get_or_create(id=1)
	setting = user.setting

	seralizer = UserSerailizer(setting, many=False)

	return JsonResponse(seralizer.data, safe=False)


def updateTheme(request):
	data = json.loads(request.body)
	theme = data['theme']
	
	user, created = User.objects.get_or_create(id=1)
	user.setting.value = theme
	user.setting.save()
	print('Request:', theme)
	return JsonResponse('Updated..', safe=False)