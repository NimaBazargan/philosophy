from django.shortcuts import render, redirect
from blog.models import Post,Gallery, Comment
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from blog.forms import CommentForm
from django.contrib import messages


def single_view(request,**kwargs):
    posts = Post.objects.filter(status = 1, published_date__lte = timezone.now())
    post = get_object_or_404(posts,id=kwargs['pid'])
    gallerys = Gallery.objects.filter(post=post)
    comments = Comment.objects.filter(post=kwargs['pid'], approved=True)
    if kwargs.get('cid'):
        parent = kwargs['cid']
    else: 
        parent = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'success')
        else:
            for errors in form.errors.values():
                for error in errors:
                    messages.add_message(request,messages.ERROR,f'{error}')
        return redirect('blog:single',pid=post.id)
    else:
        form = CommentForm()
    context = {
        'post' : post,
        'gallerys' : gallerys,
        'comments': comments,
        'form':form,
        'parent': parent,
    }
    return render(request,'blog/single.html',context)

def index_view(request,**kwargs):
    posts = Post.objects.filter(status = 1, published_date__lte = timezone.now()).order_by('-published_date')
    gallerys = Gallery.objects.all()
    if kwargs.get('type'):
        posts = posts.filter(type__type = kwargs['type'])
    if kwargs.get('cat_name'):
        posts = posts.filter(category__name = kwargs['cat_name'])
    if kwargs.get('tag_name'):
        posts = posts.filter(tag__name__in = [kwargs['tag_name']])
    if kwargs.get('author_username'):
        posts = posts.filter(author__username = kwargs['author_username'])
    if request.method == 'GET':
        if q := request.GET.get('q'):
            posts = posts.filter(content__contains = q)
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
