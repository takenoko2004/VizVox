from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('post/', views.ListPostView.as_view(), name='list-post'),
    path('post/<int:pk>/detail/', views.DetailPostView.as_view(), name='detail-post'),
    path('post/create/', views.CreatePostView.as_view(), name='create-post'),
    path('post/<int:pk>/delete/', views.DeletePostView.as_view(), name='delete-post'),
    path('post/<int:pk>/update/', views.UpdatePostView.as_view(), name='update-post'),
]