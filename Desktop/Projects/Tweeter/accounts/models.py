from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile_avatar = models.ImageField(default='profile/default-avatar.png', upload_to='profile')

    def __str__(self):
        return self.username
