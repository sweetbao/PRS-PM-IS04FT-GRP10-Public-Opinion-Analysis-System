from rest_framework import serializers,generics
from .models import Tweet

class TweetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tweet
        fields = "__all__"



