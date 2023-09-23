

from rest_framework import serializers
from apis.models import  NewUser
from apis.utils import Util
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style = {'input_type':'password'} ,write_only= True)
    class Meta:
        model = NewUser
        fields = ['fname' ,'lname' ,'mobileNumber','password','password2','tc' ,'email',"social_login"]
        extra_kwargs = {
            'password':{'write_only':True}
        }
        
    def validate(self ,data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and confirm password is not match")
        return data
    
    def create(self ,validate_data):
        return NewUser.objects.create_user(**validate_data)  
    

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255,)
    class Meta:
        model = NewUser
        fields = ['password','email',"social_login"]

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ['id','fname' ,'lname' , 'mobileNumber' ,'email',"social_login"]



class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password', 'password2']
    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return data

        
class UserSendResetPasswoedemailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255,)
    class Meta:
        fields = ['email']
    def validate(self, data):
        email = data.get('email')
        if NewUser.objects.filter(email = email).exists():
            user = NewUser.objects.get(email = email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            # print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)
            link = 'http://localhost:8000/api/v1/user/reset-password/'+uid+'/'+token
            print('Password Reset Link', link ,user)
            # Send EMail
            body = 'Click Following Link to Reset Your Password '+link
            data = {
                'subject':'Reset Your Password',
                'body':body,
                'to_email':user.email
            }
            Util.send_email(data)
            return data
        else:
            raise serializers.ValidationError('You are not a Registered User')
    
    
    

    
            
class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, data):
    try:
      password = data.get('password')
      password2 = data.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      id = smart_str(urlsafe_base64_decode(uid))
      user = NewUser.objects.get(id=id)
      print(user, token ,uid)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      return data
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')
  
