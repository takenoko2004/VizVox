from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView, 
    CreateView, 
    DeleteView,
    UpdateView,
    )
from .models import Post

class ListPostView(ListView):
    template_name = 'post/post_list.html'
    model = Post

class DetailPostView(DetailView):
    template_name = 'post/post_detail.html'
    model = Post

class CreatePostView(CreateView):
    template_name = 'post/post_create.html'
    model = Post
    fields = ('title', 'text', 'choice1', 'choice2')
    success_url = reverse_lazy('list-post')

class DeletePostView(DeleteView):
    template_name = 'post/post_confirm_delete.html'
    model = Post
    success_url = reverse_lazy('list-post')

class UpdatePostView(UpdateView):
    template_name = 'post/post_update.html'
    model = Post
    fields = ('title', 'text', 'choice1', 'choice2')
    success_url = reverse_lazy('list-post')

def index_view(request):
    object_list = Post.objects.all()
    return render(request, 'post/index.html', {'object_list': object_list})
