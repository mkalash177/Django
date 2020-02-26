from rest_framework import serializers

from application_system.models import *


class StatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statement
        fields = '__all__'


class NewCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewComment
        fields = '__all__'
