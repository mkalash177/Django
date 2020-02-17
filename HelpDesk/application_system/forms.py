from django.forms import ModelForm

from application_system.models import *


#           """форма заявки"""
class StatementCreateForm(ModelForm):
    class Meta:
        model = Statement
        # fields = ['importance', 'topic', 'text','user']
        exclude = ['user', 'progress', 'is_active']


# class DecisionCreateForm(ModelForm):
#     class Meta:
#         model = Decision
#         # fields = ['comment']
#         exclude = ['decision', 'is_active']


class CommentForm(ModelForm):
    class Meta:
        model = NewComment
        fields = ['content']
        # exclude = ['comments', 'author']
