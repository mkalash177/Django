from django.db import models
from django.contrib.auth.models import AbstractUser

SEX = (
    ('Man', 'Man'),
    ('Woman', 'Woman')
)

class MyUser(AbstractUser):
    sex = models.CharField(choices=SEX, max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.username}"

