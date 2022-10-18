from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from .models import Tweet, Topic
from .serializers import TweetSerializer, TopicSerializer
from .service import get_latestTopic, tweetSearch
from .SentimentModel.infer import get_prediction


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all().order_by('-retrievetime')
    serializer_class = TweetSerializer

    def get_queryset(self):
        title = self.request.query_params.get("title", None)
        if title:
            qs = Tweet.objects.filter()
            qs = qs.filter(title=title)

            return qs

        return super().get_queryset()


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all().order_by('rank')
    serializer_class = TopicSerializer


def addTopic(request):
    topicList = get_latestTopic()
    Topics = []
    rank = 1
    for topic in topicList:
        topicN = Topic(rank=rank, name=topic)
        topicN.save()
        rank = rank + 1
    return


def tweetsSearch(request, name):
    data = tweetSearch(name)
    a = get_prediction(data)
    prediction = countNumber(a)
    print(prediction)


    return HttpResponse('添加成功')


def countNumber(dataList):
    positive = 0
    neutral = 0
    negative = 0

    for data in dataList:
        if data == 'Positive':
            positive = positive + 1
        elif data == 'Neutral':
            neutral = neutral + 1
        elif data == 'Negative':
            negative = negative + 1

    return {'positive':positive,'neutral':neutral,'negative':negative}
