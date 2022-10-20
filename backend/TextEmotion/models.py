from pickle import TRUE
from django.db import models


# Create your models here.
class Tweet(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    comment = models.TextField()
    attitude=models.CharField(max_length=50,null=True)
    retrievetime = models.DateTimeField(auto_now_add=TRUE)

    class Meta:
        db_table = "Twitters"

    def __str__(self):
        return self.name


class Topic(models.Model):
    rank = models.IntegerField()
    name = models.TextField()
    time = models.DateTimeField(auto_now_add=TRUE)
    positiveNumber = models.IntegerField()
    negativeNumber = models.IntegerField()
    neutralNumber = models.IntegerField()
    historyRank = models.TextField(default='')

    class Meta:
        db_table = "Topics"

    def __str__(self):
        return self.name
