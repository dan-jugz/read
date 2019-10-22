from django.shortcuts import render
from django.views.generic import (CreateView,ListView,UpdateView)
from .models import Post

#login required mixins to add login required to the class based views
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

# Create your views here.


# class based home view
class HomeListView(ListView):    
    
    model=Post
    template_name='awards/home.html'
    context_object_name='sites'
    ordering=['-date_posted']
    paginate_by=4



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