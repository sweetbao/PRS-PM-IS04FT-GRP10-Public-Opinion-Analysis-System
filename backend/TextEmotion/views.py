import json

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from .models import Tweet, Topic
from .serializers import TweetSerializer, TopicSerializer
from .service import get_latestTopic, tweetSearch, tweetsGet, randomPick, addTopic, countNumber
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
    queryset = queryset[:10]
    serializer_class = TopicSerializer


def tweetsSearch(request, name):

    data = tweetSearch(name)
    a = get_prediction(data)
    tweetsList, tagLists = randomPick(data, a)
    result = []
    for i in range(0, len(tweetsList), 1):
        dic = {'text': tweetsList[i], 'tags': tagLists[i]}
        result.append(dic)
    print(a)
    prediction = countNumber(a)
    json_response = {'tweets': result, 'prediction': prediction}
    json_response = json.dumps(json_response)
    return HttpResponse(json_response, content_type="application/json")

    # print(prediction)
    # tweetsRunningJob()
    #addTopic()

    return




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
        a = topicList[count]
        a.neutralNumber = predictdata['neutral']
        a.negativeNumber =predictdata['negative']
        a.positiveNumber = predictdata['positive']
        count = count + 1
        a.save()
        print(a)
        picktweets,pickTags = randomPick(list,result)
        for i in range(0,len(picktweets),1):
            Tweet()

    return resultlist




'''
try:
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default", replace_existing=True)

    django_job_store = DjangoJobStore()
    print(django_job_store.get_all_jobs())

    #    register_events(scheduler)
    # 启动定时器
    scheduler.start()

except Exception as e:
    print('定时任务异常：%s' % str(e))'''
