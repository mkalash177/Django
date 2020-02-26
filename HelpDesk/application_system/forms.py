from django.forms import ModelForm

from application_system.models import *


#           """форма заявки"""
class StatementCreateForm(ModelForm):
    class Meta:
        model = Statement

        exclude = ['user', 'progress', 'is_active', 'cause']

class Cause(ModelForm):
    class Meta:
        model = NewComment

        fields = ['content']


class CommentForm(ModelForm):
    class Meta:
        model = NewComment
        exclude=['statements','author']


