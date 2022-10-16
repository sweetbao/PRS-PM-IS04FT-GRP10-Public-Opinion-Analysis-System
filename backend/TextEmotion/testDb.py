from django.http import HttpResponse

from .models import Topic


# 数据库操作
def testdb(request):
    test1 = Topic(rank = 1 ,name = 'hahaha')
    test1.save()
    return HttpResponse("<p>数据添加成功！</p>")