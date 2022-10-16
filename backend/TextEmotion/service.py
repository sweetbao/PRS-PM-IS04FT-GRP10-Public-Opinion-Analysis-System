import requests
from bs4 import BeautifulSoup
import re
import os
import json
import time


def is_contains_english(str):
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
    count = 1
    while len(topic_list) < 10:
        print(len(topic_list) + 1)
        a = soup.find('a', class_="tweet", rank=count).text
        count = count + 1
        if is_contains_english(a):
            topic_list.append(a)
            print(a)

    return topic_list
