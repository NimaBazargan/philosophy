from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User

class Type(models.Model):
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.type

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    title = models.CharField(max_length=255)
    type = models.ForeignKey(Type,on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/',null=True,blank=True)
    video = models.FileField(upload_to='blog/video/',null=True,blank=True)
    # audio = models.FileField(upload_to='blog/audio/',null=True,blank=True)
    category = models.ManyToManyField(Category)
    author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    published_date = models.DateTimeField(null=True)
    views = models.BigIntegerField(default=0)
    tag = TaggableManager()
    status = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    # class Meta:
    #     ordering = ['-published_date']

    def __str__(self):
        return f"{self.title} - {self.id}"
    
class Gallery(models.Model):
    post = models.ForeignKey(Post,related_name='gallery',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog/')

    def __str__(self):
        return self.post.title

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    name = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    email = models.EmailField()
    subject = models.CharField(max_length=255,null=True,blank=True)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.id}"
