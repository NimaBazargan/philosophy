from django import template
from blog.models import Post, Gallery
from django.utils import timezone
from django.shortcuts import get_object_or_404
from taggit.models import Tag

register = template.Library()

@register.inclusion_tag('blog/lastest-post.html')
def lastest_post(arg=3):
    posts = Post.objects.filter(status = 1, published_date__lte = timezone.now())[:arg]
    gallerys = Gallery.objects.all()
    for post in posts:
        if post.type.type == "Gallery":
            for gallery in gallerys:
                if gallery.post.id == post.id:
                    post.image = gallery.image
                    break

    context = {
        'posts' : posts,
        'gallerys' : gallerys,
    }
    return context

@register.simple_tag(name='counted_views')
def function(pid):
    posts = Post.objects.filter(status = 1, published_date__lte=timezone.now())
    post = get_object_or_404(posts,id=pid)
    post.views += 1
    post.save()
    return post.views

@register.inclusion_tag('blog/popular-posts.html')
def popular_post(arg=6):
    posts = Post.objects.filter(status = 1, published_date__lte=timezone.now())
    posts = posts.order_by("-views")[:arg]
    gallerys = Gallery.objects.all()
    for post in posts:
        if post.type.type == "Gallery":
            for gallery in gallerys:
                if gallery.post.id == post.id:
                    post.image = gallery.image
                    break
    context = {
        'posts': posts,
    }
    return context

@register.simple_tag(name='time')
def function(pid):
    post = Post.objects.get(id=pid)
    current_time = timezone.now() - post.published_date
    if current_time.days < 1:
        if current_time.seconds < 3600:
            if current_time.seconds < 60:
                return f"{current_time.seconds} Seconds ago"
            else:
                return f"{int(current_time.seconds/60)} Minutes ago"
        else:
            return f"{int(current_time.seconds/3600)} Hours ago"
    if current_time.days < 31:
        if timezone.now().month == post.published_date.month:
            return f"{current_time.days} Days ago"
        else:
            if timezone.now().day < post.published_date.day:
                return f"{current_time.days} Days ago"
    if current_time.days < 366 :
        if not (timezone.now().month == post.published_date.month and timezone.now().day == post.published_date.day):
            now = post.published_date.date()
            return now.strftime("%d %b")
        else:
            return post.published_date.strftime("%d %b %y")
    else:
        return post.published_date.strftime("%d %b %y")
    
@register.inclusion_tag('blog/tag.html')
def show_tags():
    tags = Tag.objects.all()
    context = {
        'tags' : tags
    }
    return context