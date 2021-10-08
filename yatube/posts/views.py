from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
# from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


from .models import Post, Group, User
from .forms import PostForm

# User = get_user_model()


# Create your views here.
def index(request):
    template = 'posts/index.html'
    #posts = Post.objects.all()[:10]
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, template, context)


@login_required
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=user)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = Post.objects.filter(author=user).count()
    # Здесь код запроса к модели и создание словаря контекста
    context = {
        'user': user,
        'page_obj': page_obj,
        'count': count
    }
    return render(request, 'posts/profile.html', context)


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    count = Post.objects.filter(author=post.author).count()
    context = {
        'post': post,
        'count': count
    }
    return render(request, 'posts/post_detail.html', context) 


@login_required
def post_create(request):
    form = PostForm(request.Post or None)
    select_group = Group.objects.all()
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.author
        post.save()
        return redirect('posts:profile', request.user)
    context = {
        'form': form,
        'select_group': select_group,
    }
    return render(request, 'posts/create_post.html', context)