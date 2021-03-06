from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)
from .models import Post, Comment, Photo
from users.forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm
from django.utils import timezone
from .forms import CommentForm, UploadForm
from django.contrib.auth.decorators import login_required

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'post/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'post/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'post/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def PostCommentView(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            context = {
        'posts': Post.objects.all()
        }
            return render(request, 'post/home.html', context)
    else:
        form = CommentForm()
    return render(request, 'post/post_comment.html', {'form': form})

def about(request):
    return render(request, 'post/about.html', {'title': 'About'})

@login_required
def upload(request, pk):

    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES) # ???????????? ???????????? ???????????? ????????? ??? ??????????????? ???????????????.
        if form.is_valid():
            photo = form.save(commit=False) # photo????????? ???????????? ?????? DB??? ?????? ???????????? ??????
            photo.author = request.user      # request.user??? ???????????? ?????????
            form.save()
            context = {
                'posts': Post.objects.all()
        }
            return render(request, 'post/home.html', context)
    else:
        form = UploadForm()
    return render(request, 'post/upload.html', {'form': form})

class IndexView(ListView):     
    template_name = 'post/post_detail.html'
     # model = Photo ????????? ????????? ???????????? ???????????? ?????? photo????????? ???????????? ????????? ????????? ?????? ????????? ????????????.
    context_object_name = 'user_post_detail' # ???????????? ???????????? ??????

    def get_queryset(self):
        user = self.request.user    # ????????????????????? ?????????
        return user.photo_set.all().order_by('-pub_date')
