from django.urls import path, include

from application_system.views import *

urlpatterns = [
    path('create/', StatementCreateView.as_view(), name='statement_create_url'),
    path('', IndexTemplateView.as_view(), name='index_url'),
    path('statement/', StatementListView.as_view(), name='statement_list_url'),
    path('change/<int:pk>', StatementChargeView.as_view(), name='statement_change_url')
]

# statement_list_url
