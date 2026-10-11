from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    DetailView, 
    CreateView, 
    DeleteView,
    UpdateView,
    )
from .models import Post, Comment, Vote, Like, Save
from django.db.models import Count, Q

class DetailPostView(LoginRequiredMixin, DetailView):
    template_name = 'post/post_detail.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = self.object

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

        if self.request.user.is_authenticated:
            post.has_voted = Vote.objects.filter(
                post=post,
                user=self.request.user
            ).exists()

            post.has_liked = Like.objects.filter(
                post=post,
                user=self.request.user
            ).exists()

            post.has_saved = Save.objects.filter(
                post=post,
                user=self.request.user
            ).exists()

        else:
            post.has_voted = False
            post.has_liked = False
            post.has_saved = False

        choice = self.request.GET.get('choice')

        comments = Comment.objects.filter(
            post=post,
            parent__isnull=True
        ).prefetch_related('replies__user')

        """
        comments = Comment.objects.filter(
            post=post,
            parent__isnull=True
        )で返信ではない親のコメントを複数とってくる。
        .prefetch_related('replies__user')によってその親コメントの
        返信とその返信をしたユーザーを取得する。
        prefetch_relatedを使うとその2回の情報取得のみで済む。
        """

        if choice == '1':
            comments = comments.filter(choice=1)

        elif choice == '2':
            comments = comments.filter(choice=2)

        context['comments'] = comments

        return context

class CreateCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ('text',)
    template_name = 'post/comment_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(pk=self.kwargs['post_id'])
        context['post'] = post

        parent_id = self.request.GET.get('parent')

        if parent_id:
            context['parent_comment'] = Comment.objects.filter(
                pk=parent_id,
                post=post
            ).first()

        return context

    def form_valid(self, form):
        form.instance.user = self.request.user

        post = Post.objects.get(pk=self.kwargs['post_id'])

        vote = Vote.objects.filter(
            post = post,
            user = self.request.user
        ).first()

        if not vote:
            form.add_error(
                None,
                'コメントするには、先に投票してください。'
            )
            return self.form_invalid(form)

        form.instance.post = post
        form.instance.choice = vote.choice

        parent_id = self.request.GET.get('parent')

        if parent_id:
            parent_comment = Comment.objects.filter(
                pk=parent_id,
                post=post
            ).first()
        # parent_commentは返信先のコメント
        
        if not parent_comment:
            form.add_error(
                None,
                '返信先のコメントが見つかりません'
            )
            return self.form_invalid(form)
        
        form.instance.parent = parent_comment

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('detail-post', kwargs={'pk': self.object.post.id})

class DeleteCommentView(LoginRequiredMixin, DeleteView):
    template_name = 'post/comment_confirm_delete.html'
    model = Comment
    
    def test_func(self):
        comment = self.get_object()
        return comment.user == self.request.user

    def get_success_url(self):
        return reverse('detail-post', kwargs={'pk': self.object.post.pk})

class UpdateCommentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'post/comment_update.html'
    model = Comment
    fields = ('text',)
    
    def test_func(self):
        comment = self.get_object()
        return comment.user == self.request.user
    
    def get_success_url(self):
        return reverse('detail-post', kwargs={'pk': self.object.post.pk})

class CreatePostView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'post/post_create.html'
    model = Post
    fields = ('title', 'text', 'choice1', 'choice2', 'image_choice1', 'image_choice2')
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
    
        return super().form_valid(form)

class DeletePostView(LoginRequiredMixin, DeleteView):
    template_name = 'post/post_confirm_delete.html'
    model = Post
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user:
            raise PermissionDenied

        return obj

class UpdatePostView(LoginRequiredMixin, UpdateView):
    template_name = 'post/post_update.html'
    model = Post
    fields = ('title', 'text', 'choice1', 'choice2', 'image_choice1', 'image_choice2')
    # success_url = reverse_lazy('list-post')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user:
            raise PermissionDenied

        return obj

    def get_success_url(self):
        return reverse('detail-post', kwargs={'pk': self.object.id})

def index_view(request):
    object_list = Post.objects.annotate(
        total_vote=Count('votes')
    )

    q = request.GET.get('q', '')

    if q:
        object_list = object_list.filter(
            Q(title__icontains=q) |
            Q(text__icontains=q)
        )

    sort = request.GET.get('sort')

    if sort == 'new':
        object_list = object_list.order_by('-created_at')
    else:
        object_list = object_list.order_by('-total_vote')

    for post in object_list:
        post.choice1_count = Vote.objects.filter(
            post=post,
            choice=1
        ).count()

        post.choice2_count = Vote.objects.filter(
            post=post,
            choice=2
        ).count()

        if post.total_vote > 0:
            post.choice1_percent = round(
                post.choice1_count / post.total_vote * 100
            )
            post.choice2_percent = 100 - post.choice1_percent
        else:
            post.choice1_percent = 0
            post.choice2_percent = 0

        if request.user.is_authenticated:
            post.has_voted = Vote.objects.filter(
                post=post,
                user=request.user
            ).exists()

            post.has_liked = Like.objects.filter(
                post=post,
                user=request.user
            ).exists()

            post.has_saved = Save.objects.filter(
                post=post,
                user=request.user
            ).exists()

        else:
            post.has_voted = False
            post.has_liked = False
            post.has_saved = False

    return render(request, 'post/index.html', {'object_list': object_list})

def vote_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        choice = request.POST.get('choice')
        if not Vote.objects.filter(post=post, user=request.user).exists():
            Vote.objects.create(
                post=post,
                user=request.user,
                choice=choice
            )

    if request.POST.get('next') == 'detail':
        return redirect('detail-post', pk=post.pk)

    return redirect('index')

def like_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    post = Post.objects.get(pk=pk)

    like = Like.objects.filter(
        post=post,
        user=request.user
    )

    if like.exists():
        like.delete()
    else:
        Like.objects.create(
            post=post,
            user=request.user
        )

    if request.POST.get('next') == 'detail':
        return redirect('detail-post', pk=post.pk)
    
    return redirect('index')

def save_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    post = Post.objects.get(pk=pk)

    save = Save.objects.filter(
        post=post,
        user=request.user
    )

    if save.exists():
        save.delete()
    else:
        Save.objects.create(
            post=post,
            user=request.user
        )

    if request.POST.get('next') == 'detail':
        return redirect('detail-post', pk=post.pk)
    
    return redirect('index')

class SavedPostView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'post/post_saved.html'

    def get_queryset(self):
        object_list = Post.objects.filter(
            saves__user=self.request.user
        )

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

            if self.request.user.is_authenticated:
                post.has_voted = Vote.objects.filter(
                    post=post,
                    user=self.request.user
                ).exists()

                post.has_liked = Like.objects.filter(
                    post=post,
                    user=self.request.user
                ).exists()

                post.has_saved = Save.objects.filter(
                    post=post,
                    user=self.request.user
                ).exists()

            else:
                post.has_voted = False
                post.has_liked = False
                post.has_saved = False
            
        return object_list