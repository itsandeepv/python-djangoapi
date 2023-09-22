

from rest_framework import serializers
from apis.models import TestApi 

class TestSerializer(serializers.HyperlinkedModelSerializer):
    user_id = serializers.ReadOnlyField()
    class Meta:
        model = TestApi
        fields = '__all__'
        
        
# class NewUserSerializer(serializers.HyperlinkedModelSerializer):
#     user_id = serializers.ReadOnlyField()
#     class Meta:
#         model = NewUser
#         fields = '__all__'