from django.forms import ModelForm

from application_system.models import Statement


#           """форма заявки"""
class StatementCreateForm(ModelForm):
    class Meta:
        model = Statement
        fields = ['importance', 'topic', 'text','user']
        # exclude = ['user']
