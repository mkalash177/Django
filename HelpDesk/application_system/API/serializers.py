from rest_framework import serializers

from application_system.models import *


class StatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statement
        fields = ['id', 'importance', 'topic', 'text', 'user', 'progress']


# class DecisionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Decision
#         fields = ['id', 'decision', 'is_active', 'comment']
