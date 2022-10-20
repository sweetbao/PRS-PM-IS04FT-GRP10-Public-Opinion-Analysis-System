import time

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from .models import Tweet, Topic
from .serializers import TweetSerializer, TopicSerializer
from .service import get_latestTopic, tweetSearch, tweetsGet
from .SentimentModel.infer import get_prediction
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_job, register_events


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


def addTopic():
    topicList = get_latestTopic()
    Topics = []
    rank = 1
    for topic in topicList:
        topicN = Topic(rank=rank, name=topic)
        # topicN.save()
        rank = rank + 1
    return topicList


def tweetsSearch(request, name):
    # data = tweetSearch(name)
    # a = get_prediction(data)
    # prediction = countNumber(a)
    # print(prediction)
    tweetsRunningJob()
    #findChange(name)

    return HttpResponse('添加成功')


def tweetsRunningJob():
    print("start to fetch")
    topicList = addTopic()
    allList = tweetsGet(topicList)
    resultlist = []
    count = 0
    for list in allList:
        result = get_prediction(list)
        predictdata = countNumber(result)
        print(predictdata)
        resultlist.append(predictdata)
        topic = topicList[count]
        historyRank = findChange(topic,count)
        a = Topic(name=topic, rank=count+1, positiveNumber=predictdata['positive'],
                  neutralNumber=predictdata['neutral'],
                  negativeNumber=predictdata['negative'],historyRank = historyRank)
        count = count + 1
        a.save()
        print(a)

    return resultlist


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

    return {'positive': positive, 'neutral': neutral, 'negative': negative}


def findChange(topic,currentRank):
    listTopic = Topic.objects.filter(name=topic).order_by('time')
    history = ''
    for topic in listTopic:
        history = history + str(topic.rank)
    if history == '':
        history = str(currentRank)
    return history


try:
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default", replace_existing=True)

    django_job_store = DjangoJobStore()
    print(django_job_store.get_all_jobs())

    #    register_events(scheduler)
    # 启动定时器
    scheduler.start()

except Exception as e:
    print('定时任务异常：%s' % str(e))
