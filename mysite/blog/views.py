from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin #? to require login for a class based views
from django.contrib.auth.decorators import login_required #? to require login for function based views

from django.urls import reverse_lazy

# Create your views here.
class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(ListView):
    model = Post
    """
    This get_queryset function gives us the opportunity to use django's built-in queryset API
    *commands such as Entry.objects.all(), Entry.objects.values()
    In this particular case, we gon' use it to get all posts; 
        which have published_date before now(the time the request is made)
        ?that is where __lte (less than or equal to ) comes in
    After getting those posts we order them from most recent (descending order) using
        ?the '-' sign before the argument('published_date') in the order_by function 
    """
    def get_queryset(self):
        return Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin,CreateView):
    """
    *This is a view that enables a logged on user to create posts.
    !The user must be logged on hence inheritance from LoginRequiredMixin 
    """

    login_url = '/login/' #? url for logging in if not already logged in
    redirect_field_name = 'blog/post_detail.html' #? url to redirect to after post creation
    
    form_class = PostForm
    model = Post


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    model = Post
    form_class = PostForm


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


class DraftListView(ListView, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    
    model = Post
    
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull = True).order_by('created_date')


#################################
##                             ##
##    FUNCTION BASED VIEWS     ##
##                             ##
#################################

# todo: function view to add a comment to a post
@login_required
def add_comment_to_post(request, pk):
    # ? to get the specific(using its pk) post that the comment would be associated with
    # if not found then a 404 page would be returned
    post = get_object_or_404(Post, pk = pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            #? (commit = False) saves the form object to memory but not to the database
            comment = form.save(commit = False) 
            comment.post = post
            comment.save()
            return redirect('post_detail', pk = post.pk)
    else:
        form = CommentForm()    
    return render(request, 'blog/comment_form.html',{'form':form})


# todo: function view to approve a comment
@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail', pk = comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    post_pk = comment.post.pk #? necessary because you cannot access the comment's comment.post.pk 
                              #? after deleting the comment
    comment.delete()
    return redirect('post_detail', pk = post_pk)
    

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post, pk = pk)
    post.publish()
    return redirect('post_detail', pk = pk)


