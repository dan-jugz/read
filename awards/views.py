from django.shortcuts import render
from django.views.generic import (CreateView)

# Create your views here.

def home(request):
       return render(request,'awards/home.html')



class PostCreateView(LoginRequiredMixin,CreateView):
    '''
        using class based view to create a post
        args:CreateView from django.views.generic
    ''' 
    model=Post
    fields=['title','description','link','image'] 
    template_name='awards/post-new.html'  
    success_url='/'