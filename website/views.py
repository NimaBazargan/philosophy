from django.shortcuts import render, redirect
from blog.models import Post, Gallery
from django.utils import timezone
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from website.forms import ContactForm, NewsletterForm
from django.contrib import messages

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
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            modify_name = 'unknown'
            my_model = form.save(commit=False)
            my_model.name = modify_name
            my_model.save()
            messages.add_message(request,messages.SUCCESS,'success')
        else:
            for errors in form.errors.values():
                for error in errors: 
                    messages.add_message(request,messages.ERROR,f'{error}')
    else:        
        form = ContactForm()
    context = {
        'form' : form
    }
    return render(request,'website/contact.html',context)

def newsletter_view(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            next_url = request.POST.get('next')
            return redirect(next_url)
    return redirect(next_url)