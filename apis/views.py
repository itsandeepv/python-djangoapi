from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from apis.models import TestApi 
from apis.serializers import TestSerializer 

class TestViewSet(viewsets.ModelViewSet):
    queryset = TestApi.objects.all()
    serializer_class = TestSerializer
    
    
# class NewUserViewSet(viewsets.ModelViewSet):
#     queryset = NewUser.objects.all()
#     serializer_class = NewUserSerializer
