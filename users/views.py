from django.shortcuts import render

# Create your views here.

# view function for a user profile
@login_required
def profile(request):
    
    

    user=User.objects.get(pk=request.user.id)
    posts=user.post_set.all()
    context={
        'usr_form':usr_form,
        'prof_form':prof_form,
        'posts':posts
    }

    

    return render(request,'users/profile.html',context)