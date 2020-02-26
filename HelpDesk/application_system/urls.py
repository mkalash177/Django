
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from application_system.views import *
from application_system.API.resourses import *

router = DefaultRouter()
router.register(r'statement-api', StatementViewSet)
router.register(r'comment-api', NewCommentViewSet)

urlpatterns = [
    path('create/', StatementCreateView.as_view(), name='statement_create_url'),
    path('', IndexTemplateView.as_view(), name='index_url'),
    path('statement/', StatementListView.as_view(), name='statement_list_url'),
    path('change/<int:pk>', StatementChargeView.as_view(), name='statement_change_url'),
    path('statement/answer/<int:pk>', AnswerDecision.as_view(), name='accept_decision'),
    path('statement/acceptlist', AcceptDecisionList.as_view(), name='accept_decision_url'),
    path('statement/rejecttlist', RejectDecisionList.as_view(), name='reject_decision_url'),
    path('statement/renewlist', RenewListView.as_view(), name='renew_decision_url'),
    path('statement/statementndetail/<int:pk>', StatementDetail.as_view(), name='statement_detail_url'),
    path('createcomment/', CommentCreateView.as_view(), name='comment_create'),
    path('', include(router.urls)),

]
