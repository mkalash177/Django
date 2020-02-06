from django.db import models
from django.contrib.auth.models import AbstractUser

# SEX = (
#     ('Man', 'Man'),
#     ('Woman', 'Woman'),
#     ('Unknown', 'Unknown')
# )


class MyUser(AbstractUser):
    # birthday = models.DateTimeField()
    # sex = models.CharField(choices=SEX, max_length=10)

    def __str__(self):
        return f"{self.username}"

