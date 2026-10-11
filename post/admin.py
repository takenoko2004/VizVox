from django.contrib import admin
from .models import Post, Comment, Vote, Like, Save

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(Like)
admin.site.register(Save)