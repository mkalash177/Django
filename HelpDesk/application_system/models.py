from django.db import models

# Create your models here.
from authenticate.models import MyUser

IMORTANCE = (
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High')
)


#           """Модель заявки"""
class Statement(models.Model):
    importance = models.CharField(choices=IMORTANCE, max_length=6)
    topic = models.CharField(max_length=255)
    text = models.TextField(max_length=500)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)


#           """Результат решения"""
class Decision(models.Model):
    decision = models.ForeignKey(Statement, on_delete=models.CASCADE)
