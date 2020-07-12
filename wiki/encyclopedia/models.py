from django.db import models
from django.conf import settings

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length = 64)
    description = models.TextField()

    def publish(self):
        self.save()

    def __str__(self):
        return self.title
