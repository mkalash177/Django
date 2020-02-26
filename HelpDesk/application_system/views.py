from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView, DeleteView, DetailView

from application_system.forms import *
from application_system.models import *
from rest_framework import viewsets
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

    # def post(self, request, *args, **kwargs):
    #     self.statement = Statement.objects.get(id=kwargs.get('statement_id'))
    #     return super().post(request, *args, **kwargs)


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


class AcceptDecision(CreateView, UserPassesTestMixin):
    model = Statement
    success_url = '/statement/acceptlist'
    template_name = 'application_system/statement_list.html'
    form_class = StatementCreateForm
    request_obj = None

    def post(self, request, *args, **kwargs):
        item = Statement.objects.get(id=kwargs.get('pk'))
        item.progress = 'Рассмотрено'
        item.is_active = 1
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
        # return super().post(request, *args, **kwargs)
        return redirect(self.success_url)

    def test_func(self):
        if self.request.user.is_superuser:
            return self.request.user.is_superuser

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
    model = Statement
    template_name = 'application_system/accept_decision.html'
    queryset = Statement.objects.filter(is_active=1).order_by('-importance')
    context_object_name = 'accept_lists'


class RejectDecision(CreateView, UserPassesTestMixin):
    model = Statement
    success_url = '/statement'
    template_name = 'application_system/statement_list.html'
    form_class = StatementCreateForm
    request_obj = None

    def post(self, request, *args, **kwargs):
        item = Statement.objects.get(id=kwargs.get('pk'))
        item.progress = 'Рассмотрено'

        item.cause = self.request.POST.get('cause')
        item.is_active = 2
        item.save()
        return redirect(self.success_url)

    def test_func(self):
        if self.request.user.is_superuser:
            return self.request.user.is_superuser


class RejectDecisionList(ListView):
    model = Statement
    template_name = 'application_system/reject_decision.html'
    queryset = Statement.objects.filter(is_active__in=[2, 4]).order_by('-importance')
    context_object_name = 'reject_lists'

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context.update({
    #         'cause': Cause
    #     })
    #     return context


class RenewCreateView(CreateView):
    model = Statement
    success_url = '/statement'
    template_name = 'application_system/reject_decision.html'
    form_class = StatementCreateForm

    def post(self, request, *args, **kwargs):
        renews = Statement.objects.get(id=kwargs.get('pk'))
        renews.progress = 'В обработке'
        # renews.cause = self.request.POST.get('cause')
        renews.is_active = 3
        renews.save()
        return redirect(self.success_url)


class RenewListView(ListView):
    model = Statement
    template_name = 'application_system/renew_list.html'
    queryset = Statement.objects.filter(is_active=3).order_by('-importance')
    context_object_name = 'renew_list'


class RenewAcceptView(CreateView, UserPassesTestMixin):
    model = Statement
    template_name = "application_system/renew_list.html"
    success_url = '/statement/renewlist'
    form_class = StatementCreateForm
    renews = None
    request_obj = None

    def post(self, request, *args, **kwargs):
        renews = Statement.objects.get(id=kwargs.get('pk'))
        renews.is_active = 1
        renews.save()
        return redirect(self.success_url)

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context.update({
    #         'cause': Cause
    #     })
    #     return context

    def test_func(self):
        if self.request.user.is_superuser:
            return self.request.user.is_superuser


class RenewARejectView(CreateView, UserPassesTestMixin):
    model = Statement
    template_name = "application_system/renew_list.html"
    success_url = '/statement/renewlist'
    form_class = StatementCreateForm
    renews = None
    request_obj = None

    def post(self, request, *args, **kwargs):
        renews = Statement.objects.get(id=kwargs.get('pk'))
        renews.is_active = 4
        renews.progress = 'откончательно решено'
        renews.save()
        return redirect(self.success_url)

    def test_func(self):
        if self.request.user.is_superuser:
            return self.request.user.is_superuser


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
