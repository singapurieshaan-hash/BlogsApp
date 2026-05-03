from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required 
from django.http import Http404 

from .models import Blog, BlogPost

from .forms import BlogForm, BlogPostForm  

def index(request):
    return render(request, 'blogs/index.html') 

@login_required 
def blogpage(request):
    blogs = Blog.objects.filter(owner=request.user).order_by('date_added')
    context = {'blogs' : blogs}
    return render(request,'blogs/blogpage.html',context)

@login_required
def blogposts(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    if blog.owner != request.user:
        raise Http404 
    post = blog.blogpost_set.order_by('-date_added')
    context = {'blog': blog, 'post': post}
    return render(request, 'blogs/blogposts.html',context)

@login_required 
def new_blog(request):
    if request.method != 'POST':
        form = BlogForm()
    else:
        form = BlogForm(data=request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.owner = request.user
            new_user.save()
            return redirect('blogs:blogpage')

    context = {'form': form}
    return render(request, 'blogs/new_blog.html', context)

@login_required 
def new_blogposts(request, blog_id):
    blog = Blog.objects.get(id=blog_id)

    if request.method != 'POST':
       form = BlogPostForm()
    else:
       form = BlogPostForm(data=request.POST)
       if form.is_valid():
          new_blogposts = form.save(commit=False)
          new_blogposts.blog = blog 
          new_blogposts.save()
          return redirect('blogs:blogposts', blog_id=blog.id)
    
    context = {'blog':blog,'form':form}
    return render(request, 'blogs/new_blogposts.html', context)

@login_required 
def edit_post(request, pot_id):
    blogpost = BlogPost.objects.get(id=pot_id)
    blog = blogpost.blog
    if blog.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = BlogPostForm(instance=blogpost)
    else:
        form = BlogPostForm(instance=blogpost, data=request.POST)
        if form.is_valid():
            form.save()
        return redirect('blogs:blogposts',blog_id=blog.id)

    context= {'blog':blog,'form':form,'blogpost':blogpost}
    return render(request,'blogs/edit_post.html',context)


        



