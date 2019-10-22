from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

class Profile(models.Model):
    
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    bio=models.TextField(max_length=140,blank=True)
    profile_photo=models.ImageField(upload_to='profile_pics',default='default_profile.png',blank=True)
    
    def __str__(self):
        return f'{self.user.username}-Profile'