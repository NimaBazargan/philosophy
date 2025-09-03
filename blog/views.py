from django.shortcuts import render
from blog.models import Post,Gallery
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage


def sigle_view(request,pid):
    posts = Post.objects.filter(status = 1, published_date__lte = timezone.now())
    post = get_object_or_404(posts,id=pid)
    gallerys = Gallery.objects.filter(post=post)
    context = {
        'post' : post,
        'gallerys' : gallerys,
    }
    return render(request,'blog/single.html',context)

def index_view(request,**kwargs):
    posts = Post.objects.filter(status = 1, published_date__lte = timezone.now())
    gallerys = Gallery.objects.all()
    if kwargs.get('type'):
        posts = posts.filter(type__type = kwargs['type'])
    posts = Paginator(posts,4)
    try:
        page_number = request.GET.get('page')
        posts = posts.get_page(page_number)
    except PageNotAnInteger:
        posts = posts.get_page(1)
    except EmptyPage:
        posts = posts.page(posts.num_pages)
    context = {
        'posts' : posts,
        'gallerys' : gallerys,
    }
    return render(request,'blog/blog-home.html',context)
