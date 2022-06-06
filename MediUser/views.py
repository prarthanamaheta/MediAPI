from django.contrib.auth import login
from django.contrib.auth.models import User

from rest_framework import generics, status, views
from rest_framework.response import Response

from MediUser import serializers
from .models import MediUser
from MediUser.serializers import MediRegisterSerializer, MediLoginSerializer


class MediUserRegister(generics.CreateAPIView):
    queryset = MediUser.objects.all()
    serializer_class = MediRegisterSerializer


class MediUserLogin(views.APIView):
    serializer_class = MediLoginSerializer
    query_set = User.objects.all()


    def post(self, request):
        serializer = serializers.MediLoginSerializer(data=self.request.data,
                                                     context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response('success', status=status.HTTP_202_ACCEPTED)
