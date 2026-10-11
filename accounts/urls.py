from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

from .views import SignupView

app_name = 'accounts'

urlpatterns = [
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('profile_update/', views.ProfileUpdateView.as_view(), name='update-profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
]