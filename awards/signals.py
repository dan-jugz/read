#signal fired after an obj is saved in this cas when a user is created
from django.db.models.signals import post_save

#post to sende the signal
from .models import Post

#reciever of the signal
from django.dispatch import receiver

from .models import Review


@receiver(post_save,sender=Post)
def create_review(sender,instance,created,**kwargs):

    '''
        post_save:is the signal that is fired after and object is saved
        Post:model is the sender of the signal
        receiver:is the create rating function that fetches the signal and performs some task
        instance:is the instance of Post class
        created : if a post  was created
    '''
    if created:
        Review.objects.create(post=instance)