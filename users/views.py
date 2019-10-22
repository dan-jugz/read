from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegistrationForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required

# Create your views here.

# view function for registering 
def register(request):
    
    
    if request.method=='POST':
         form=UserRegistrationForm(request.POST)

         if form.is_valid():
             form.save()
             username=form.cleaned_data.get('username')
             messages.success(request,f'Account for {username} created!')
             return redirect('login')

    else:
        form=UserRegistrationForm()
    
    return render(request,'users/registration.html',{'form':form})


# view function for a user profile
@login_required
def profile(request):
    
    
    # instance=request.user populating the fields with the current user details
    if request.method=='POST':
        usr_form=UserUpdateForm(request.POST,instance=request.user)
        prof_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        
        if usr_form.is_valid and prof_form.is_valid:
            usr_form.save()
            prof_form.save()
            messages.success(request,f'Your Account Has Been Updated')

            return redirect('profile')
    else:
        usr_form=UserUpdateForm(instance=request.user)
        prof_form=ProfileUpdateForm(instance=request.user.profile)

    user=User.objects.get(pk=request.user.id)
    posts=user.post_set.all()
    context={
        'usr_form':usr_form,
        'prof_form':prof_form,
        'posts':posts
    }

    

    return render(request,'users/profile.html',context)