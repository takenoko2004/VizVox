from django.contrib import admin
from .models import Post, Comment, Vote, Like

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(Like)