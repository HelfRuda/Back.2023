from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from .models import Post, Category, Tag, Comments
from .form import CommentsForm, PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from .form import RegistrationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from .spamcheck import SpamCheck 
from django.http import HttpResponse

class AllPostsView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name='Admins').exists()

    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'blog/all_posts.html', {'posts': posts})
    
class AddPostView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name='Admins').exists()

    def get(self, request):
        form = PostForm()
        return render(request, 'blog/add_post.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('all_posts')
        return render(request, 'blog/add_post.html', {'form': form})
    
class EditPostView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name='Admins').exists()

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(instance=post)
        return render(request, 'blog/edit_post.html', {'form': form})

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('all_posts')
        return render(request, 'blog/edit_post.html', {'form': form})

class DeletePostView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name='Admins').exists()
    
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'blog/delete_post.html', {'object': post})

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect('all_posts')

class RegistrationView(View):
    template_name = 'blog/registration.html'

    def get(self, request):
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
        return render(request, self.template_name, {'form': form})
    
class LoginView(View):
    template_name = 'blog/login.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        return render(request, self.template_name, {'form': form})

class TagView(View):
    def get(self, request):
        tag = Tag.objects.all()
        return render(request, 'blog/blog.html', {'tag_list': tag})

class CategoryView(View):
    def get(self, request):
        category = Category.objects.all()
        return render(request, 'blog/category.html', {'category_list': category})

class PostView(View):
    def get(self, request, category_id=None):
        if category_id:
            posts = Post.objects.filter(category_id=category_id)
        else:
            posts = Post.objects.all()
        return render(request, 'blog/blog.html', {'post_list': posts})
    
class PostDetail(View):
    def get(self, request, category_id, pk):
        post = Post.objects.get(id=pk)
        return render(request, 'blog/blog_detail.html', {'post': post})
    
class AddComments(LoginRequiredMixin, View):
    def post(self, request, category_id, pk):
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data['text_comment']  # Получаем текст комментария
            if SpamCheck.is_spam(comment_text):  # Проверяем на спам
                return HttpResponse('Ваш комментарий содержит спам и не может быть опубликован.')
            
            form = form.save(commit=False)
            form.post_id = pk
            form.user = request.user
            form.save()
            post_url = reverse('blog_detail', kwargs={'category_id': category_id, 'pk': pk})
            return redirect(post_url)
        return redirect('/')