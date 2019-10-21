from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

# Create your models here.
class Post(models.Model):
    
    title=models.CharField(max_length=30)
    description=models.TextField()
    link=models.CharField(max_length=100)
    image=models.ImageField(upload_to='poster/',default='')
    date_posted=models.DateTimeField(auto_now_add=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    design=models.IntegerField(blank=True,default=0)
    usability=models.IntegerField(blank=True,default=0)
    creativity=models.IntegerField(blank=True,default=0)
    content=models.IntegerField(blank=True,default=0)
    mobile=models.IntegerField(blank=True,default=0)
    
    def __str__(self):
        return f'Post{self.title}--{self.description}--{self.author.username}'




    # method to save a post
    def save_post(self):
            
        self.save()


    # method to fetch all posts
    @classmethod
    def get_posts(cls):
        
        posts=cls.objects.order_by('-date_posted')
        return posts   


    @classmethod
    def get_post_by_id(cls,id):
        try:

            post=cls.objects.get(id=id)
        except ObjectDoesNotExist:

            raise Http404()
            assert False