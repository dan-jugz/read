from django.urls import path
from .views import (PostCreateView,UserPostListView,PostUpdateView,PostDeleteView)
from . import views
from django.conf.urls import url

urlpatterns=[
    path('', views.home ,name='awards-home'), 
    path('post/new/',PostCreateView.as_view(),name='post-new'),
    path('user/<str:username>/posts',UserPostListView.as_view(),name='user-posts'),
    path('post/<int:pk>/',views.postDetail,name='post-detail'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(),name='post-delete'),
    path('search/',views.search_results,name='search-results'),
    url(r'^api/posts/$', views.PostList.as_view()),
    url(r'api/posts/post-id/(?P<pk>[0-9]+)/$',views.PostDescription.as_view()),
    url(r'^api/profiles/$', views.ProfileList.as_view()),
]