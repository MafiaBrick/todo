from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Todo(models.Model):
    title = models.CharField(max_length=150)
    memo = models.TextField(blank = True)
    impotantFlag = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add = True)
    datecompleat = models.DateTimeField(null=True)
