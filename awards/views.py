from django.shortcuts import render
from django.views.generic import (CreateView,ListView,UpdateView)
from .models import Post

#login required mixins to add login required to the class based views
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

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

    # setting up the user instance to the form being submitted so it doesnt raise the intergrity error
    def form_valid(self,form):
        
        form.instance.author=self.request.user
        return super().form_valid(form)

# class view to render user posts
class UserPostListView(ListView):
    
    model=Post
    template_name='awards/user-posts.html'
    context_object_name='sites'
    ordering=['-date_posted']
    paginate_by=5

    def get_queryset(self):
      
        user= get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.get_posts_by_username(user)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):  
     
    model=Post
    fields=['title','description','link','image'] 
    template_name='awards/post-new.html'  
    
    # setting up the user instance to the form being submitted so it doesnt raise the intergrity error
    def form_valid(self,form):
        
        form.instance.author=self.request.user
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
   
    model=Post
    success_url='/'
    context_object_name='site'
    template_name='awards/post-confirm-delete.html'

    