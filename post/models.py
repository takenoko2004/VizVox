from django.db import models

class Post(models.Model):
    text = models.TextField()
    choice1 = models.CharField(max_length=100)
    image_choice1 = models.ImageField(null=True, blank=True)
    choice2 = models.CharField(max_length=100)
    image_choice2 = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class Vote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    choice = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['post', 'user'],
                name='unique_vote'
            )
        ]

    def __str__(self):
        return f'{self.user} - {self.post} - 選択肢{self.choice}'