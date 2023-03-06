from django.urls import path
from .views import *

# from ..check_valid.check_information import *
app_name='Accounts'

urlpatterns=[
    #authenticated
    path('login_register',ShowFormLoginRegisterView.as_view(),name='login_register'),
    path('login',LoginView.as_view(),name='login'),
    path('logout',LogoutView.as_view(),name='logout'),
    path('register',RegisterView.as_view(),name='register'),
    path('verify_otp_code',OtpCodeView.as_view(),name='otp'),


        # #resetpassword
    path('password/reset/',PasswordResetView.as_view(),name='passwordreset'),
    path('password/reset/done',PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password/reset/confirm/<uidb64>/<token>/',PasswordResetConfirm.as_view(),name='password_reset_confirm'),
    path('password/reset/complate',PasswordResetComplateView.as_view(),name='password_reset_complate'),
    
    path('contact',ContactView.as_view(),name='contact'),
    path('quastion',QuestionsView.as_view(),name='quastion'),
    path('answer',Answer_QuestionsView.as_view(),name='answer'),
    path('profile',UserProfileView.as_view(),name='profile'),
    path('check/information/',Check_Information_View.as_view(),name='emailexist'),




   

    


]