from rest_framework import viewsets

from application_system.API.serializers import StatementSerializer, NewCommentSerializer
from application_system.models import Statement, NewComment


class StatementViewSet(viewsets.ModelViewSet):
    queryset = Statement.objects.all().order_by('-importance')
    serializer_class = StatementSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()


class NewCommentViewSet(viewsets.ModelViewSet):
    queryset = NewComment.objects.all()
    serializer_class = NewCommentSerializer

    def perform_create(self, serializer):
        serializer.save()
