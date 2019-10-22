from django.shortcuts import render
from django.views.generic import (CreateView,ListView,UpdateView,DeleteView)
from .models import Post,Review
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import NewReviewForm
from django.contrib import messages
from users.models import Profile

#login required mixins to add login required to the class based views
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

# area api
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import PostSerializer
from .serializer import ProfileSerializer
from rest_framework import status

# Create your views here.

@login_required
def home(request):

    sites_list=Post.get_posts()
    paginator = Paginator(sites_list, 5)
    page = request.GET.get('page')
    sites = paginator.get_page(page)

    return render(request,'awards/home.html',{'sites':sites})

# class based home view
# class HomeListView(ListView):    
    
#     model=Post
#     template_name='awards/home.html'
#     context_object_name='sites'
#     ordering=['-date_posted']
#     paginate_by=4



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

    # check if current user is the author of the post
    def test_func(self):
    
        post=self.get_object()

        if self.request.user==post.author:
            return True
        return False    

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
   
    model=Post
    success_url='/'
    context_object_name='site'
    template_name='awards/post-confirm-delete.html'


    # check if current user is the author of the post
    def test_func(self):
    
        post=self.get_object()

        if self.request.user==post.author:
            return True
        return False    

# view function that leads to a single post
def postDetail(request,pk):

    post=Post.get_post_by_id(pk)
    reviews=Review.get_all_reviews(pk)

    post.design=reviews['design']
    post.usability=reviews['usability']
    post.creativity=reviews['creativity']
    post.content=reviews['content']
    post.mobile=reviews['mobile']
    post.average_review=reviews['average_review']

    post.save()


    current_user=request.user
    if request.method=='POST':
        form=NewReviewForm(request.POST)
        if form.is_valid():
            review=form.save(commit=False)
            review.judge=current_user
            review.post=post
            
            review.save()
            messages.success(request,f'Review Submitted')

            return redirect('post-detail',pk)

    else:
        form=NewReviewForm()  

    context={
        'site':post,
        'form':form
    }

    return render(request,'awards/post-detail.html',context)


# view function that redirects to a search results page
def search_results(request):    
    
    if 'site' in request.GET and request.GET['site']:
        search_term=request.GET.get('site')
        search_posts=Post.search(search_term)
        context={
            'message':f'{search_term}',
            'sites':search_posts
        }

        return render(request,'awards/search.html',context)
    else :
        return render(request,'awards/search.html')    



class PostList(APIView):
    def get(self,request,format=None):
        all_posts=Post.objects.all()
        serializers=PostSerializer(all_posts,many=True)
        return Response(serializers.data)

# Api view to fetch a single post
class PostDescription(APIView):         

    def get_post(self,pk):
        
        try:
            return Post.objects.get(pk=pk)

        except Post.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        post = self.get_post(pk)
        serializers = PostSerializer(post)
        return Response(serializers.data)        
   


class ProfileList(APIView):

    def get(self,request,format=None):