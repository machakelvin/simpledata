# models.py
from django.db import models
from django.contrib.auth.models import User

class Entry(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    date = models.DateField()
    quantity = models.IntegerField(default=0)
    details = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
