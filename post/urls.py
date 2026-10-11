from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('post/<int:pk>/vote/', views.vote_view, name='vote'),
    path('post/<int:pk>/detail/', views.DetailPostView.as_view(), name='detail-post'),
    path('post/create/', views.CreatePostView.as_view(), name='create-post'),
    path('post/<int:pk>/delete/', views.DeletePostView.as_view(), name='delete-post'),
    path('post/<int:pk>/update/', views.UpdatePostView.as_view(), name='update-post'),
    path('post/<int:post_id>/comment/', views.CreateCommentView.as_view(), name='comment'),
    path('comment/<int:pk>/delete/', views.DeleteCommentView.as_view(), name='delete-comment'),
    path('comment/<int:pk>/update/', views.UpdateCommentView.as_view(), name='update-comment'),
    path('post/<int:pk>/like/', views.like_view, name='like'),
    path('post/<int:pk>/save/', views.save_view, name='save'),
    path('post/saved/', views.SavedPostView.as_view(), name='saved-post')
]