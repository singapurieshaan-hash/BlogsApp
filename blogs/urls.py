from django.urls import path 
from . import views 

app_name = 'blogs'

urlpatterns = [
    #Home page 
    path('', views.index, name= 'index'),
    path('blogpage/', views.blogpage, name= 'blogpage'),
    path('blogposts/<int:blog_id>', views.blogposts, name= 'blogposts'),
    path('new_blog/', views.new_blog, name= 'new_blog'),
    path('new_blogposts/<int:blog_id>', views.new_blogposts, name='new_blogposts'),
    path('edit_blogposts/<int:pot_id>', views.edit_post, name='edit_post'),
]
