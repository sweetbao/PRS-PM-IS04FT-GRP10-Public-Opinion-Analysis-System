import json

from datetime import datetime
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from .models import Tweet, Topic
from .serializers import TweetSerializer, TopicSerializer
from .service import get_latestTopic, tweetSearch, tweetsGet,  addTopic, countNumber
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
    queryset = Topic.objects.all().order_by('-time')
 
    serializer_class = TopicSerializer
    def get_queryset(self):
        Latest = self.request.query_params.get("isLatest", None)
        if Latest:
            return super().get_queryset()[:10]
        else:
            return super().get_queryset()

def tweetsSearch(request, name):

    data = tweetSearch(name)
    data = sorted(data,key=lambda t:t[1],reverse=True)
    text = []
    like = []
    for i in range(0,len(data),1):
        text.append(data[i][0])
        like.append(data[i][1])
    a = get_prediction(text)
    result = []
    require = 30
    if len(data)<30:
        require = len(data)
    for i in range(0, require, 1):
        dic = {'comment': text[i], 'attitude': a[i],'like':like[i]}
        result.append(dic)
    print(a)
    result = sorted(result,key=lambda t:t['like'])
    prediction = countNumber(a)
    json_response = {'tweets': result, 'prediction': prediction}
    json_response = json.dumps(json_response)
    return HttpResponse(json_response, content_type="application/json")
    '''
        tweetsRunningJob()
        return HttpResponse(status=200)
    '''


    # print(prediction)

    #addTopic()

   # return HttpResponse(status=200)'''

def getText(request, id):
    topic = Topic.objects.get(id = id)
    tweets = Tweet.objects.filter(topic = topic.name)
    rank = topic.rank
    print(rank)
    print(type(rank))
    name = topic.name
    positiveNumber = topic.positiveNumber
    negativeNumber = topic.negativeNumber
    neutralNumber = topic.neutralNumber
    tweetsList = []
    for i in tweets:
        textdata = {'like': i.like, 'comment': i.comment, 'attitude': i.attitude}
        tweetsList.append(textdata)
    topicdata = {'rank':rank,'name':name,'positiveNumber':positiveNumber,'negativeNumber':negativeNumber,'neutralNumber':neutralNumber}
    data = sorted(tweetsList,key=lambda t:t['like'])
    jsonfile = {'tweets':tweetsList,'topic':topicdata}
    json_str = json.dumps(jsonfile)
    return HttpResponse(json_str, content_type="application/json")


def getTopic(request):
    queryset = Topic.objects.all().order_by('-time')
    a = queryset[:10]
    topicList = []
    for t in a:
        print(type(t.rank))
        print(t.rank)
        dic = {'id':t.pk,'timestamp':t.time.strftime("%d-%b-%Y (%H:%M)") , 'amount':t.volume, 'rank':t.rank,'name':t.name,'positiveNumber':t.positiveNumber,'negativeNumber':t.negativeNumber,'neutralNumber':t.neutralNumber}
        topicList.append(dic)
    result = sorted(topicList,key=lambda t:t['rank'])

    json_response = {'topics': result}
    json_response = json.dumps(json_response)
    return HttpResponse(json_response, content_type="application/json")






def tweetsRunningJob():
    print("start to fetch")
    topicList = addTopic()
    nameList = []
    for topic in topicList:
        nameList.append(topic.name)

    allList = tweetsGet(nameList)
    print(len(allList))
    resultlist = []
    count = 0
    for i in range(0,len(allList),1):
        list = allList[i]
        text = []
        like = []
        for m in  range(0,len(list),1):
            text.append(list[m][0])
            like.append(list[m][1])
        result = get_prediction(text)
        predictdata = countNumber(result)
        print(predictdata)
        resultlist.append(predictdata)
        a = topicList[count]
        a.neutralNumber = predictdata['neutral']
        a.negativeNumber =predictdata['negative']
        a.positiveNumber = predictdata['positive']
        count = count + 1
        a.save()
        print(a)
        require = 30
        if len(text)<30:
            require = len(text)
        for j in range(0,require,1):
            tweet = Tweet(topic = nameList[i],like = like[j],comment = text[j],attitude = result[j])
            tweet.save()
    return resultlist




try:
    django_job_store = DjangoJobStore()
    print(django_job_store.get_all_jobs())
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default", replace_existing=True)
   # django_job_store = DjangoJobStore()
  #  print(django_job_store.get_all_jobs())
   # django_job_store.remove_all_jobs()


    @register_job(scheduler, 'cron', id='sixjob', hour=6, minute=0)
    def sixAm():

        print('job1')
        tweetsRunningJob()


    @register_job(scheduler, 'cron', id='eightjob', hour=8, minute=0)
    def eightAm():

        print('job2')
        tweetsRunningJob()


    @register_job(scheduler, 'cron', id='test3', hour=10, minute=0)
    def tenAm():

        print('job3')
        tweetsRunningJob()


    @register_job(scheduler, 'cron', id='test4', hour=12, minute=0)
    def tweAm():

        print('job4')
        tweetsRunningJob()


    @register_job(scheduler, 'cron', id='test5', hour=14, minute=0)
    def twopm():

        print('job5')

        tweetsRunningJob()


    @register_job(scheduler, 'cron', id='test6', hour=16, minute=0)
    def fourpm():

        print('job6')
        tweetsRunningJob()


    @register_job(scheduler, 'cron', id='test7', hour=18, minute=0)
    def sixpm():

        print('job7')
        tweetsRunningJob()


    @register_job(scheduler, 'cron', id='test8', hour=20, minute=0)
    def eightpm():

        print('job8')
        tweetsRunningJob()


    @register_job(scheduler, 'cron', id='test9', hour=22, minute=0)
    def tenpm():

        print('job9')
        tweetsRunningJob()



   # django_job_store.remove_all_jobs()





    #    register_events(scheduler)
    # 启动定时器
    scheduler.start()

except Exception as e:
    print('定时任务异常：%s' % str(e))
