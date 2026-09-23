from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    DetailView, 
    CreateView, 
    DeleteView,
    UpdateView,
    )
from .models import Post, Comment

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

class CreateCommentView(CreateView):
    model = Comment
    fields = ('post', 'text')
    template_name = 'post/comment_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.get(pk=self.kwargs['post_id'])

        return context

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('detail-post', kwargs={'pk': self.object.post.id})