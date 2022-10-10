from pickle import TRUE
from django.db import models

# Create your models here.
class Tweet(models.Model):
    title = models.CharField( max_length=100)
    author = models.CharField( max_length=50)
    comment = models.TextField()
    retrievetime = models.DateTimeField( auto_now_add=TRUE)

    class Meta:
        db_table="Twitters"

    def __str__(self):
        return self.name
