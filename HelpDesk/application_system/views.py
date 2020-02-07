from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView, DeleteView

from application_system.forms import StatementCreateForm, DecisionCreateForm
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

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect(self.success_url)

    # def post(self, request, *args, **kwargs):
    #     self.statement = Statement.objects.get(id=kwargs.get('statement_id'))
    #     return super().post(request, *args, **kwargs)


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
    queryset = Statement.objects.all().order_by('-importance')
    context_object_name = 'lists'

    def get_queryset(self):
        if not self.request.user.is_superuser:
            queryset = Statement.objects.filter(info_user_id=self.request.user.id)
            return queryset
        return super().get_queryset()


class AcceptDecision(CreateView):
    model = Statement
    success_url = '/statement/acceptlist'
    template_name = 'application_system/statement_list.html'
    form_class = DecisionCreateForm
    decision = None

    def post(self, request, *args, **kwargs):
        decisions = Statement.objects.get(id=kwargs.get('id'))
        decisions.progress = 'Рассмотрено'
        item = Decision()
        item.decision = decisions
        gtrue = True
        bfalce = False
        if item.is_active == gtrue:
            return HttpResponseRedirect(self.success_url)
        elif item.is_active == bfalce:
            return HttpResponseRedirect(self.success_url)
        item.save()
        decisions.save()
        return redirect(self.success_url)

    # def form_valid(self, form):
    #     obj = form.save(commit=False)
    #     obj.user = self.request.user
    #     obj.decision = self.decision
    #     obj.save()
    #     return HttpResponseRedirect(self.success_url)


class AcceptDecisionList(ListView):
    model = Decision
    template_name = 'application_system/accept_decision.html'
    queryset = Decision.objects.all()
    context_object_name = 'accept_lists'


class RejectDecision(CreateView):
    model = Decision
    success_url = '/statement'
    template_name = 'application_system/statement_list.html'
    form_class = DecisionCreateForm
