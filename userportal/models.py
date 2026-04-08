import random
import string
import uuid
from django.db import models, IntegrityError
from django.contrib.auth.models import User

def generate_team_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8)) #randomly we are generating team id of size 8 A-Z a-z 0-9


class Team(models.Model):
    team_id = models.CharField(max_length=8, primary_key=True, editable=False)
    team_name = models.CharField(max_length=100, unique=True)

    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='teams')

    def save(self, *args, **kwargs):
        if not self.team_id:
            while True:
                try:
                    self.team_id = generate_team_id()
                    super().save(*args, **kwargs)
                    break
                except IntegrityError:
                    continue
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.team_name

def generate_post_id():
    return uuid.uuid4().hex[:20]

class Post(models.Model):
    post_id = models.CharField(
        max_length=20,
        primary_key=True,
        default=generate_post_id,
        editable=False
    )

    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True)
    pdf = models.FileField(upload_to='pdfs/', blank=True, null=True)

    summary = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.team.team_name}"
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)