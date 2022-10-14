import re
import emoji
import simplejson as simplejson
from urllib3.packages.six import unichr


def sentenceClean(sentence):
    # check web link inside or not
    sentence = str(sentence)
    if 'https' in sentence:
        sentence = sentence.split('https')[0]
        print(sentence)
    # replace the \n and tag
    sentence = re.sub(r'[(\n)(#)]', ' ', sentence)
    sentence = filter_emoji(sentence)


    return sentence


def filter_emoji(desstr, restr=''):
    # filt emoji
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)




