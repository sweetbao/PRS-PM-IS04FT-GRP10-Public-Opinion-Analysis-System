import random

import requests
from bs4 import BeautifulSoup
import re
import json
from .dataClean import sentenceClean
import time
from pygtrans import Translate

from .models import Topic

bearer_token1 = 'AAAAAAAAAAAAAAAAAAAAAH6%2FhgEAAAAAC174stDAGI%2FLK7FVJCUdZNIXdr8%3DBddrVjoAkoV2erXv1tZCFWSM7oBYsotbCWWa56AmkVKADFnGHQ'
bearer_token2 = 'AAAAAAAAAAAAAAAAAAAAAB9aiQEAAAAAl%2BIItIjyrWrejGzyCIs%2FOpcaoHU%3DxEY2Of52bmPFcr4X0w7E6DUjtgHuG0TNT84zEQ7MP2yPJMb1Ab'

search_url = "https://api.twitter.com/2/tweets/counts/recent"

# Optional params: start_time,end_time,since_id,until_id,next_token,granularity
query_params = {'query': 'from:twitterdev', 'granularity': 'day'}


def is_contains_english(str):
    if len(str) > 20:
        return False
    my_re = re.compile(r'[A-Za-z]', re.S)
    res = re.findall(my_re, str)
    if len(res):
        return True
    else:
        return False


def get_latestTopic():
    res = requests.get('https://twitter-trends.iamrohit.in/singapore')
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')

    topic_list = []
    volume_list = []
    count = 1
    while len(topic_list) < 10:
        print(len(topic_list) + 1)
        fullText = soup.find('a', class_="tweet", rank=count)

        a = fullText.text
        b = fullText.get('tweetc')
        volume_list.append(b)
        count = count + 1
        if is_contains_english(a):
            a = a.replace('#', '')
            topic_list.append(a)
            print(a)
    volume_list = handleStr(volume_list)

    return topic_list, volume_list


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token1}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def bearer_oauth2(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token2}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules(number):
    if number == 1:
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth,
        )
    else:
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth2,
        )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    # print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules, number):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    if number == 1:
        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            auth=bearer_oauth,
            json=payload
        )
    else:
        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            auth=bearer_oauth2,
            json=payload
        )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(delete, trendings, number):
    # You can adjust the rules if needed

    sample_rules = [
        # {"value": "dog has:images", "tag": "dog pictures"},
        {"value": trendings, "tag": trendings},

    ]
    payload = {"add": sample_rules}
    if number == 1:
        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            auth=bearer_oauth,
            json=payload,
        )
    else:
        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            auth=bearer_oauth2,
            json=payload,
        )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_stream(set, number, account):
    client = Translate()
    dataSet = []
    startTime = time.perf_counter()
    print(startTime)
    if account == 1:
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/stream?tweet.fields=lang,public_metrics,referenced_tweets&expansions=referenced_tweets.id&media.fields=public_metrics",
            auth=bearer_oauth, stream=True,
        )
    else:
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/stream?tweet.fields=lang,public_metrics,referenced_tweets&expansions=referenced_tweets.id&media.fields=public_metrics",
            auth=bearer_oauth2, stream=True,
        )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )

    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            a = json.dumps(json_response, indent=4, sort_keys=True)
            tweetsText = str(json_response['includes']['tweets'][0]['text'])
            langage = str(json_response['data']['lang'])
            like = json_response['data']['public_metrics']['like_count']
            print(langage)
            # print(a)
            if langage in ['qme', 'qmt', 'und', 'hi', 'tl', 'und', 'art']:
                continue
            if tweetsText.__contains__('RT @'):
                try:
                    tweetsText = json_response['includes']['tweets'][1]['text']
                except:
                    continue
            texts = client.translate(tweetsText, target='en', fmt='text')
            if not texts is None:
                texts = texts.translatedText
            else:
                continue
            print(tweetsText)
            print('here is trans')
            print(texts)
            tweetsText = sentenceClean(texts)
            if tweetsText == '':
                continue
            print(tweetsText)
            dataSet.append((tweetsText, like))
            print(len(dataSet))
            if number == 199:
                nowTime = time.perf_counter()
                # print(nowTime-startTime)
                # print(len(dataSet))
                if nowTime - startTime > 180:
                    response.close()
                    dataSet = sorted(dataSet, key=lambda t: t[1], reverse=True)
                    return dataSet
            # print(len(dataSet))
            if number == 999:
                nowTime = time.perf_counter()
                if nowTime - startTime > 300:
                    response.close()
                    dataSet = sorted(dataSet, key=lambda t: t[1], reverse=True)
                    return dataSet
            if len(dataSet) > number:
                response.close()
                dataSet = sorted(dataSet, key=lambda t: t[1], reverse=True)
                return dataSet

    return dataSet


def tweetsGet(trendings):
    targetData = []
    for i in range(0, 10, 1):
        if i < 5:
            number = 2
        else:
            number = 1
        rules = get_rules(number)
        delete = delete_all_rules(rules, number)
        print(delete)
        print(trendings[i])
        print(number)
        set = set_rules(delete, trendings[i], number)
        print('good')
        target = get_stream(set, 199, number)

        targetData.append(target)
        print('finish ' + str(trendings[i]))

    return targetData


def tweetSearch(keywords):
    rules = get_rules(1)
    delete = delete_all_rules(rules, 1)
    trendings = keywords
    set = set_rules(delete, trendings, 1)
    target = get_stream(set, 199, 1)
    return target


def addTopic():
    topicList, volumeList = get_latestTopic()
    Topics = []
    rank = 1
    for i in range(0, len(topicList)):
        topicN = Topic(rank=rank, name=topicList[i], volume=volumeList[i])
        # topicN.save()
        rank = rank + 1
        Topics.append(topicN)
    return Topics


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


def handleStr(numberlist: list):
    result = []
    for i in numberlist:
        if i.startswith('Under'):
            i = i.split(' ')[1]
        num = float(i[:-1])
        if i[-1] == 'K':
            num = num * 1000
        elif i[-1] == 'M':
            num = num * 1000000
        result.append(int(num))
    return result
