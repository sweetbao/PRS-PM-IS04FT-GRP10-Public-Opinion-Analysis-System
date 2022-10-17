import re



def sentenceClean(sentence):
    # check web link inside or not
    sentence = str(sentence)
    if 'https' in sentence:
        sentence = sentence.split('https')[0]
    # replace the \n and tag
    sentence = re.sub(r'[(\n)]', ' ', sentence)
    sentence = filter_emoji(sentence)
    sentence = filter_kor(sentence)
    sentence = specialEmoji(sentence)


    return sentence


def filter_emoji(desstr, restr=''):
    # filt emoji
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)

def specialEmoji(sentence):
    sentence  = re.sub(u"([^\u0041-\u005a\u0061-\u007a\u0030-\u0039])", " ", sentence)
    sentence = ' '.join(sentence.split())
    return sentence

def filter_kor(desstr, restr=''):
    try:
        kor = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\uAC00-\uD7A3]')
    except re.error:
        kor = re.compile(u'[\u3040-\u309F\u30A0-\u30FF\uAC00-\uD7A3]')
    return kor.sub(restr,desstr)


