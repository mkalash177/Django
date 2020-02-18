from rest_framework import serializers

from application_system.models import *


class StatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statement
        fields = ['id', 'importance', 'topic', 'text', 'user', 'progress']


class NewCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewComment
        fields = ['id', 'comments', 'author', 'content']
