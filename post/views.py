from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    DetailView, 
    CreateView, 
    DeleteView,
    UpdateView,
    )
from .models import Post, Comment, Vote
from django.db.models import Count

class ListPostView(ListView):
    template_name = 'post/post_list.html'
    model = Post

class DetailPostView(DetailView):
    template_name = 'post/post_detail.html'
    model = Post

class CreatePostView(CreateView):
    template_name = 'post/post_create.html'
    model = Post
    fields = ('text', 'choice1', 'choice2', 'image_choice1', 'image_choice2')
    success_url = reverse_lazy('list-post')

class DeletePostView(DeleteView):
    template_name = 'post/post_confirm_delete.html'
    model = Post
    success_url = reverse_lazy('list-post')

class UpdatePostView(UpdateView):
    template_name = 'post/post_update.html'
    model = Post
    fields = ('text', 'choice1', 'choice2', 'image_choice1', 'image_choice2')
    success_url = reverse_lazy('list-post')

def index_view(request):
    object_list = Post.objects.all()

    for post in object_list:
        post.choice1_count = Vote.objects.filter(
            post=post,
            choice=1
        ).count()

        post.choice2_count = Vote.objects.filter(
            post=post,
            choice=2
        ).count()

        post.total_vote = post.choice1_count + post.choice2_count

        if post.total_vote > 0:
            post.choice1_percent = round(
                post.choice1_count / post.total_vote * 100
            )
            post.choice2_percent = 100 - post.choice1_percent
        else:
            post.choice1_percent = 0
            post.choice2_percent = 0
        
        post.has_voted = Vote.objects.filter(
            post=post,
            user=request.user
        ).exists()

    return render(request, 'post/index.html', {'object_list': object_list})

def vote_view(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method =='POST':
        choice = request.POST.get('choice')
        if not Vote.objects.filter(post=post, user=request.user).exists():
            Vote.objects.create(
                post=post,
                user=request.user,
                choice=choice
            )
    return redirect('index')

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