from django.forms import ModelForm

from application_system.models import *


#           """форма заявки"""
class StatementCreateForm(ModelForm):
    class Meta:
        model = Statement
        # fields = ['importance', 'topic', 'text','user']
        exclude = ['user', 'progress']


class DecisionCreateForm(ModelForm):
    class Meta:
        model = Decision
        fields = ['comment']
        # exclude = ['decision', 'is_active']


# class RenewCreateForm(ModelForm):
#     class Meta:
#         model = RenewStatement
#         exclude = ['renew']
