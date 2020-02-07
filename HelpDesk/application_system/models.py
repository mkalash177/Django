from django.db import models

# Create your models here.
from authenticate.models import MyUser

IMORTANCE = (
    (1, 'Low'),
    (2, 'Medium'),
    (3, 'High')
)


#           """Модель заявки"""
class Statement(models.Model):
    importance = models.IntegerField(choices=IMORTANCE, max_length=6)
    topic = models.CharField(max_length=255)
    text = models.TextField(max_length=500)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    progress = models.CharField(max_length=100, default='')

    def __str__(self):
        return f"{self.topic},{self.text}"


#           """Результат решения"""
class Decision(models.Model):
    decision = models.OneToOneField(Statement, on_delete=models.CASCADE)
    is_active = models.NullBooleanField(default=None)

    def __str__(self):
        return f"{self.decision.topic},{self.is_active}"