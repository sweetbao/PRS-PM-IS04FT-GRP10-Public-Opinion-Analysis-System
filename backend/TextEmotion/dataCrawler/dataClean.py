def sentenceClean(sentence):
    # check web link inside or not
    sentence = str(sentence)
    if 'https' in sentence:
        sentence = sentence.split('https')[0]
        print(sentence)







    return sentence


a = 'hello world jiliguala https://t.co/qHokUYUa2D'
b = sentenceClean(a)
