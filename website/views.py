from django.shortcuts import render
from blog.models import Post, Gallery
from django.utils import timezone
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def index_view(request):
    posts = Post.objects.filter(status = 1, published_date__lte = timezone.now()).order_by('-published_date')
    gallerys = Gallery.objects.all()
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
    return render(request,'website/index.html',context)

def about_view(request):
    return render(request,'website/about.html')

def contact_view(request):
    return render(request,'website/contact.html')