from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView, DeleteView, DetailView

from application_system.forms import *
from application_system.models import *

from application_system.API.serializers import *


class IndexTemplateView(TemplateView):
    template_name = 'application_system/index.html'


class StatementCreateView(CreateView):
    model = Statement
    form_class = StatementCreateForm
    template_name = 'application_system/statement_create.html'
    success_url = '/statement'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = MyUser.objects.get(id=self.request.user.id)
        obj.save()
        return HttpResponseRedirect(self.success_url)


class StatementChargeView(UpdateView):
    model = Statement
    template_name = 'application_system/statement_change.html'
    success_url = '/statement'
    fields = ['text', 'importance']


class StatementListView(ListView):
    model = Statement
    template_name = 'application_system/statement_list.html'
    queryset = Statement.objects.all().order_by('-importance')
    context_object_name = 'lists'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'cause': Cause
        })
        return context

    def get_queryset(self):
        if not self.request.user.is_superuser:
            queryset = Statement.objects.filter(user_id=self.request.user.id)
            return queryset
        return super().get_queryset()


class AnswerDecision(CreateView, UserPassesTestMixin):
    model = Statement
    success_url = '/'
    template_name = 'application_system/statement_list.html'
    form_class = StatementCreateForm
    request_obj = None

    def post(self, request, *args, **kwargs):
        item = Statement.objects.get(id=kwargs.get('pk'))
        item.progress = 'Рассмотрено'
        form = self.get_form()
        if form.data['is_active'] == '1':
            item.is_active = 1
            item.progress = 'принято'
            item.save()
            return redirect(reverse_lazy('accept_decision_url'))
        elif form.data['is_active'] == '2':
            item.is_active = 2
            item.progress = 'отклонено'
            item.cause = self.request.POST.get('cause')
            item.save()
            return redirect(reverse_lazy('reject_decision_url'))
        elif form.data['is_active'] == '3':
            item.is_active = 3
            item.progress = 'Возобновлено'
            item.save()
            return redirect(reverse_lazy('renew_decision_url'))
        elif form.data['is_active'] == '4':
            item.is_active = 4
            item.progress = 'Окончательно решено'
            item.save()
            return redirect(reverse_lazy('reject_decision_url'))

    def test_func(self):
        self.request_obj = Statement.objects.get(pk=self.kwargs.get('pk'))
        valid_status = [1, 2, 4]
        if self.request.user.is_superuser:
            if self.request_obj.is_active in valid_status:
                return True


class AcceptDecisionList(ListView):
    model = Statement
    template_name = 'application_system/accept_decision.html'
    queryset = Statement.objects.filter(is_active=1).order_by('-importance')
    context_object_name = 'accept_lists'


class RejectDecisionList(ListView):
    model = Statement
    template_name = 'application_system/reject_decision.html'
    queryset = Statement.objects.filter(is_active__in=[2, 4]).order_by('-importance')
    context_object_name = 'reject_lists'


class RenewListView(ListView):
    model = Statement
    template_name = 'application_system/renew_list.html'
    queryset = Statement.objects.filter(is_active=3).order_by('-importance')
    context_object_name = 'renew_list'


class StatementDetail(DetailView):
    model = Statement
    template_name = 'application_system/statement_detail.html'
    context_object_name = 'statement'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context.update({'newcomments': NewComment.objects.filter(statements_id=self.object.id),
                        'comment': CommentForm})
        return context


class CommentCreateView(CreateView):
    form_class = CommentForm
    template_name = 'application_system/statement_detail.html'

    def get_success_url(self):
        return str(self.request.META.get('HTTP_REFERER'))

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.statements_id = self.request.POST.get('statement')
        obj.author = self.request.user
        obj.save()
        return redirect(self.get_success_url())
