from rest_framework import viewsets

from authenticate.API.serializers import MyUserSerializer
from authenticate.models import MyUser


class MyUserViewsets(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer

    def perform_create(self, serializer):
        serializer.save()