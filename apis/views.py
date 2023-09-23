
# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from apis.renderers import UserRenderer 
from apis.serializers import UserRegisterSerializer ,UserLoginSerializer,UserProfileSerializer,UserChangePasswordSerializer,UserSendResetPasswoedemailSerializer,UserPasswordResetSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }
  
  
class UserRegisterView(APIView):
    renderer_classes = [UserRenderer]
    def post(self ,request ,format=None):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({"message":"User Registeration Successfully"} , status=status.HTTP_201_CREATED)
        return Response(serializer.error , status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self ,request ,format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email= email ,password = password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({"message":"User Login Successfully",'accesstoken':token,} , status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.error , status=status.HTTP_400_BAD_REQUEST)
            
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'message':'Password Changed Successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
            
class UserSendResetPasswoedemailView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = UserSendResetPasswoedemailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'message':'email send to you email  Successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
            

class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    if serializer.is_valid(raise_exception=True):
        return Response({'message':'Password Reset Successfully'}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
        
        


