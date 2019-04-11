from django.shortcuts import render
#from django.http import HttpResponse
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import Synthetic_Form, DeleteForm
from django.shortcuts import redirect

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    #print(post)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = Synthetic_Form(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = Synthetic_Form()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = Synthetic_Form(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = Synthetic_Form(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_delete(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        form = DeleteForm(request.POST, instance=post)
        if form.is_valid(): # checks CSRF
            post.delete()
            return redirect('post_list')
    else:
        form = DeleteForm(instance = post)
    return render(request, 'blog/post_delete.html', {'form': form})
