from django.urls import path
from .views import (PostCreateView,UserPostListView)
from . import views

urlpatterns=[
    path('',views.home,name='awards-home'), 
    path('post/new/',PostCreateView.as_view(),name='post-new'),
    path('user/<str:username>/posts',UserPostListView.as_view(),name='user-posts'),
    path('post/<int:pk>/',views.postDetail,name='post-detail'),
    
]