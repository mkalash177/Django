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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'comment': DecisionCreateForm
        })
        return context

    def get_queryset(self):
        if not self.request.user.is_superuser:
            queryset = Statement.objects.filter(info_user_id=self.request.user.id)
            return queryset
        return super().get_queryset()


class AcceptDecision(CreateView):
    model = Decision
    success_url = '/statement/acceptlist'
    template_name = 'application_system/statement_list.html'
    form_class = DecisionCreateForm

    def post(self, request, *args, **kwargs):
        decisions = Statement.objects.get(id=kwargs.get('pk'))
        decisions.progress = 'Рассмотрено'
        item = Decision()
        item.is_active = 1
        item.decision = decisions
        # form = self.get_form()
        # form_add = form.save(commit=False)
        # if form.data['is_active'] == '1':
        #     form_add.is_active = True
        #     # return HttpResponseRedirect(self.success_url)
        # elif form.data['is_active'] == '0':
        #     form_add.is_active = False

        # if item.is_active == 1:
        #     item.is_active = True
        #     return HttpResponseRedirect(self.success_url)
        # elif item.is_active == 0:
        #     item.is_active = False
        #     return HttpResponseRedirect(self.success_url)
        # form.save()
        item.save()
        decisions.save()
        # return super().post(request, *args, **kwargs)
        return redirect(self.success_url)

    # def form_valid(self, form):
    #     # item = Decision()
    #     form_add = form.save(commit=False)
    #     if form.data['is_active'] == '1':
    #         form_add.is_active = True
    #         # return HttpResponseRedirect(self.success_url)
    #     elif form.data['is_active'] == '0':
    #         form_add.is_active = False
    #     # form_add.decision = self.model.decision
    #     # form_add.decision_id = self.kwargs['pk']
    #     form.save()
    #     return redirect(self.success_url)
    # #     return super().form_valid(form)


class AcceptDecisionList(ListView):
    model = Decision
    template_name = 'application_system/accept_decision.html'
    queryset = Decision.objects.filter(is_active=1)
    context_object_name = 'accept_lists'


class RejectDecision(CreateView):
    model = Decision
    success_url = '/statement'
    template_name = 'application_system/statement_list.html'
    form_class = DecisionCreateForm

    def post(self, request, *args, **kwargs):
        decisions = Statement.objects.get(id=kwargs.get('pk'))
        decisions.progress = 'Рассмотрено'
        item = Decision()
        item.is_active = 2
        item.decision = decisions
        item.save()
        decisions.save()
        return redirect(self.success_url)


class RejectDecisionList(ListView):
    model = Decision
    template_name = 'application_system/reject_decision.html'
    queryset = Decision.objects.filter(is_active=2)
    context_object_name = 'reject_lists'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'comment': DecisionCreateForm
        })
        return context


#### до этого момента пока норм
#### тут возобновление с ним шаманить
class RenewCreateView(CreateView):
    model = Decision
    success_url = '/statement'
    template_name = 'application_system/reject_decision.html'
    form_class = Decision

    def post(self, request, *args, **kwargs):
        renews = Decision.objects.get(id=kwargs.get('pk'))
        renews.decision.progress = 'В обработке'
        renews.is_active = 3
        renews.save()
        return redirect(self.success_url)


class RenewListView(ListView):
    model = Decision
    template_name = 'application_system/renew_list.html'
    queryset = Decision.objects.filter(is_active=3)
    context_object_name = 'renew_list'


##########################################
class RenewAcceptView(CreateView):
    model = Decision
    template_name = "application_system/renew_list.html"
    success_url = '/statement/renewlist'
    form_class = DecisionCreateForm
    renews = None

    def post(self, request, *args, **kwargs):
        renews = Decision.objects.get(id=kwargs.get('pk'))
        renews.is_active = 1
        renews.save()
        return redirect(self.success_url)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'comment': DecisionCreateForm
        })
        return context


class RenewARejectView(CreateView):
    model = Decision
    template_name = "application_system/renew_list.html"
    success_url = '/statement/renewlist'
    form_class = DecisionCreateForm
    renews = None

    def post(self, request, *args, **kwargs):
        renews = Decision.objects.get(id=kwargs.get('pk'))
        renews.is_active = 4
        renews.decision.progress = 'откончательно решено'
        renews.save()
        return redirect(self.success_url)
