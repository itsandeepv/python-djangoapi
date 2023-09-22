




from django.urls import path ,include
from apis.views import TestViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r"testapi" ,TestViewSet , basename='testapi')


urlpatterns = [
    path('', include(router.urls)),
]