from django.urls import path
from blog.views import *

app_name = 'blog'

urlpatterns = [
    path('post/<int:pid>/',sigle_view,name='single'),
    path('type/<str:type>/',index_view,name='type'),
    path('category/<str:cat_name>/',index_view,name='category'),
    path('tag/<str:tag_name>/',index_view,name='tag'),
    path('author/<str:author_username>/',index_view,name='author'),
    path('search/',index_view,name='search'),
]