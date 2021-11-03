from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views import View
from .models import Post, Comment, UserProfile
from .forms import PostForm, CommentForm
from django.views.generic.edit import UpdateView, DeleteView

# Create your views here.
class PostListView(LoginRequiredMixin, View):
    def get(self, request):
        posts = Post.objects.all().order_by('-date_posted')
        form = PostForm()

        context = {
            'post_list': posts,
            'form': form,
        }
        return render(request, 'socialmedia\post_list.html', context)

    def post(self, request):
        posts = Post.objects.all().order_by('-date_posted')
        form = PostForm(request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

        context = {
            'post_list': posts,
            'form': form,
        }
        return render(request, 'socialmedia\post_list.html', context)

class PublicPostListView(View):
    def get(self, request):
        posts = Post.objects.all().order_by('-date_posted')

        context = {
            'post_list': posts,
        }
        return render(request, 'socialmedia\public_post_list.html', context)

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
    fields = ['body']
    template_name = 'socialmedia\post_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
        

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

        context = {
            'user' : user,
            'profile' : profile,
            'posts' : post,
        }

        return render(request, 'socialmedia\profile.html', context)

class EditProfileView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    fields = ['name', 'major', 'bio', 'birth_date', 'picture']
    template_name = 'socialmedia\profile_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user