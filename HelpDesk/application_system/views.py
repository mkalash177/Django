from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

from application_system.forms import StatementCreateForm
from application_system.models import *

# Кнопка Создать Заявку на index.html
class IndexTemplateView(TemplateView):
    template_name = 'application_system/index.html'

# Создание заявки
class StatementCreateView(CreateView):
    model = Statement
    form_class = StatementCreateForm
    template_name = 'application_system/statement_create.html'
    success_url = '/statement'

# Изменение заявки
class StatementChargeView(UpdateView):
    model = Statement
    template_name = 'application_system/statement_change.html'
    success_url = '/statement'
    fields = ['text', 'importance']

# Отображает заявки залогиненого юзера
class StatementListView(ListView):
    model = Statement
    template_name = 'application_system/statement_list.html'
    queryset = Statement.objects.all()
    context_object_name = 'lists'

    def get_queryset(self):
        if not self.request.user.is_superuser:
            queryset = Statement.objects.filter(info_user_id=self.request.user.id)
            return queryset
        return super().get_queryset()
