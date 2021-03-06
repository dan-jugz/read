#signal fired when a user is created
from django.db.models.signals import post_save

#user to send the signal
from django.contrib.auth.models import User

#reciever of the signal
from django.dispatch import receiver

from .models import Profile


@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):

    if created:
        Profile.objects.create(user=instance)


# save profile once a user is saved
@receiver(post_save,sender=User)
def save_profile(sender,instance,**kwargs):
    
    instance.profile.save()