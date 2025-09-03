from django.urls import path
from blog.views import *

app_name = 'blog'

urlpatterns = [
    path('post/<int:pid>/',sigle_view,name='single'),
    path('<str:type>/',index_view,name='type'),
]