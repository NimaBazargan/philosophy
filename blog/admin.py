from django.contrib import admin
from blog.models import Category, Type, Post, Gallery, Comment
from django_summernote.admin import SummernoteModelAdmin

class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 1

class PostAdmin(SummernoteModelAdmin):
    inlines = [GalleryInline,]
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    list_display = ['title','type','author','status','views','published_date','created_date',]
    list_filter = ['status','type','author','published_date',]
    ordering = ['-published_date',]
    search_fields = ['title','content',]
    summernote_fields = ['content',]

class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    list_display = ['post','name','approved','created_date',]
    list_filter = ['post','approved',]
    search_fields = ['name','post',]


admin.site.register(Category)
admin.site.register(Type)
admin.site.register(Post,PostAdmin)
admin.site.register(Gallery)
admin.site.register(Comment,CommentAdmin)