from django.contrib.auth.models import AbstractUser
from django.db import models

from foodgram import settings


class User(AbstractUser):
    """ Custom user model """

    following = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                       related_name="his_following")

    def __str__(self):
        return f'{self.username}: {self.get_full_name()}'
