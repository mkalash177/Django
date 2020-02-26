from django.db import models

# Create your models here.
from authenticate.models import MyUser

IMORTANCE = (
    (1, 'Low'),
    (2, 'Medium'),
    (3, 'High')
)
IS_ACTIVE = (
    (1, 'Accept'),
    (2, 'Reject'),
    (3, 'Renew'),
    (4, 'completely rejected')
)


#           """Модель заявки"""
class Statement(models.Model):
    importance = models.IntegerField(choices=IMORTANCE)
    topic = models.CharField(max_length=255)
    text = models.TextField(max_length=500)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    progress = models.CharField(max_length=100, default='')
    is_active = models.CharField(choices=IS_ACTIVE, max_length=10)


    def __str__(self):
        return f"{self.topic},{self.text}"



class NewComment(models.Model):
    statements = models.ForeignKey(Statement, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    content = models.TextField(max_length=255, verbose_name='content')
