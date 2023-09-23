




from django.urls import path ,include
from apis.views import UserRegisterView,UserPasswordResetView,UserLoginView,UserProfileView,UserChangePasswordView ,UserSendResetPasswoedemailView



urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register',),
    path('login/', UserLoginView.as_view(), name='login',),
    path('profile/', UserProfileView.as_view(), name='profile',),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword',),
    path('password-reset-email/', UserSendResetPasswoedemailView.as_view(), name='send-email',),
    path('reset-password/<uid>/<token>', UserPasswordResetView.as_view(), name='reset-password',),
]