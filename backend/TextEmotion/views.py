import time

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from .models import Tweet, Topic
from .serializers import TweetSerializer, TopicSerializer
from .service import get_latestTopic, tweetSearch,tweetsGet
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
        topicN.save()
        rank = rank + 1
    return topicList


def tweetsSearch(request, name):
    data = tweetSearch(name)
    a = get_prediction(data)
    prediction = countNumber(a)
    print(prediction)


    return HttpResponse('添加成功')


def tweetsRunningJob():
    print("start to fetch")
    topicList = addTopic()
    allList = tweetsGet(topicList)
    resultlist = []
    for list in allList:
        result = get_prediction(list)
        predictdata = countNumber(result)
        print(predictdata)
        resultlist.append(predictdata)
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

    return {'positive':positive,'neutral':neutral,'negative':negative}


try:
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    timenow = time.time()


    @register_job(scheduler, 'cron', id='test1' + str(timenow) , hour=6, minute=0)
    def sixAm():

        print('job1')
        tweetsRunningJob()


    @register_job(scheduler, 'cron', id='test2' + str(timenow), hour=8, minute=0)
    def eightAm():

        print('job2')
        tweetsRunningJob()


    @register_job(scheduler, 'cron', id='test3' + str(timenow), hour=10, minute=0)
    def tenAm():

        print('job3')
        tweetsRunningJob()


    @register_job(scheduler, 'cron', id='test4' + str(timenow), hour=12, minute=0)
    def tweAm():

        print('job4')
        tweetsRunningJob()


    @register_job(scheduler, 'cron', id='test5' + str(timenow), hour=14, minute=0)
    def twopm():

        print('job5')
        tweetsRunningJob()


    @register_job(scheduler, 'cron', id='test6' + str(timenow), hour=16, minute=0)
    def fourpm():

        print('job6')
        tweetsRunningJob()


    @register_job(scheduler, 'cron', id='test7' + str(timenow), hour=18, minute=0)
    def sixpm():

        print('job7')
        tweetsRunningJob()


    @register_job(scheduler, 'cron', id='test8' + str(timenow), hour=20, minute=0)
    def eightpm():

        print('job8')
        tweetsRunningJob()


    @register_job(scheduler, 'cron', id='test9' + str(timenow), hour=22, minute=0)
    def tenpm():

        print('job9')
        tweetsRunningJob()


    @register_job(scheduler, 'cron', id='justtest' + str(timenow), hour=17, minute=28)
    def tenpm():

        print('job9')
        tweetsRunningJob()




    register_events(scheduler)
    # 启动定时器
    scheduler.start()
except Exception as e:
    print('定时任务异常：%s' % str(e))
