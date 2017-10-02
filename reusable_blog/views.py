# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404

from django.utils import timezone
from .models import Post

from .forms import BlogPostForm

from django.shortcuts import redirect


# Create your views here.
def post_list(request):
    """
    Create a view that will return a
    list of Posts that were published prior to'now'
    and render them to the 'blogposts.html' template
    """
    posts = Post.objects.filter(published_date__lte=timezone.now()
        ).order_by('-published_date')
    #print posts
    return render(request, "blog/blogposts.html", {'posts': posts})


# Create your views here.
def post_list_top5(request):
    """
    Create a view that will return the 5 most viewed
    Posts that were published prior to'now'
    and render them to the 'blogposts.html' template
    """
    posts = Post.objects.filter(published_date__lte=timezone.now()
        ).order_by('-views') [:5]
    print posts
    return render(request, "blog/blogposts.html", {'posts': posts})



def post_detail(request, id):
    """
    Create a view that return a single
    Post object based on the post ID and
    and render it to the 'postdetail.html'
    template. Or return a 404 error if the
    post is not found. It now updates the 
    views count to 1 too.
    """
    post = get_object_or_404(Post, pk=id)
    post.views += 1 # clock up the number of post views
    post.save()
    return render(request, "blog/postdetail.html", {'post': post})




    """
	We would like to redirect to the postdetail template once we have saved our post, just to see our newly created blog post entry, 
	hence the redicrect below.

	If the view was accessed because the Submit button was clicked, then it will become true that the request method is POST. 
		The form data will be saved to the database.
		Once the data is saved, we will be redirected to the postdetail view.
	Else if view was opened from a link, then:
		The GET method has seen to have been used.
		The new post form is displayed.
    """
def new_post(request):
    if request.method == "POST":
        form = form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect(post_detail, post.pk)
    else:
        form = BlogPostForm()
        return render(request, 'blog/blogpostform.html', {'form': form})



"""
This looks very much like our new_post view we created earlier. But there are a few differences which you no doubt spotted 
when typing out the code. The function take a primary key id as an extra parameter (just like the post_detail view).

Editing an item using a form is a two step process. First we need a way to get the item we want to edit into a Form in the browser. 
Then we want to process the edit when the user clicks submit.

Getting the Initial form is achieved using a HTTP GET method. Handling the submitted changed is acheived using a HTTP POST method.

Our edit_post view above handles both these scenarios and uses if request.method == “POST”: to decide which is happening.

If the method is POST then we must take the submitted details, validate them, save them to the database, and then redirect the user 
to the page that will show them the edited post.

As with the ‘new_post’ view, we need to add support for images to be attached to the blog post.
	form = BlogPostForm(request.POST, request.FILES, instance=post)
"""

def edit_post(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect(post_detail, post.pk)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog/blogpostform.html', {'form': form})


