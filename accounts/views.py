from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView
from .models import Profile
from post.models import Post, Comment, Vote, Like, Save

from .forms import SignupForm

class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile.html'

    def get_object(self):
        return Profile.objects.get(
            user_id=self.kwargs['pk']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['posts'] = Post.objects.filter(
            user=self.object.user
        )

        context['comments'] = Comment.objects.filter(
            user=self.object.user
        )

        context['tab'] = self.request.GET.get('tab', 'posts')

        for post in context['posts']:

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

        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['icon', 'bio']
    template_name = 'accounts/profile_update.html'
    
    def get_success_url(self):
        return reverse(
            'accounts:profile',
            kwargs={'pk': self.object.pk}
        )

    def get_object(self):
        return self.request.user.profile

class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        return response