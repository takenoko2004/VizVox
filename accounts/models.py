from django.db import models

class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    icon = models.ImageField(null=True, blank=True)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return self.user.username