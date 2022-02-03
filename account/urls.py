from django.urls import path
from rest_framework import routers
from .views import *

app_name = 'account'

router = routers.DefaultRouter()
# router.register('student', ealerViewSet, basename='student')
urlpatterns = [

    path('login/', LoginView.as_view() ,name= 'login'),
    path('logout/', LogoutView.as_view() ,name= 'logout'),

    path('register/', StudentRegisterView.as_view() ,name= 'register'),
    path('email-verify/', EmailVerification.as_view() ,name= 'email-verify'),
    path('forget-password-email/', ForgetPasswordEmail.as_view() ,name= 'forget-password-email'),
    path('forget-password-verify/', ForgetPasswordVerification.as_view() ,name= 'forget-password-verify'),
    path('forget-password/', ForgetPassword.as_view() ,name= 'forget-password'),
]
urlpatterns += router.urls 