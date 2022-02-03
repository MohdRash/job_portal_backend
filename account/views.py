from django.shortcuts import render
from account.serializers import *
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate,logout
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from account.models import OtpVerification

from student.models import Student
from random import randint
from django.core.mail import  EmailMultiAlternatives

# Create your views here.
class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self,request):
        context = {}
        username = request.data.get('username')
        password = request.data.get('password')
        account = authenticate(username=username, password=password)

        if account:
            try:
                token = Token.objects.get(user=account)
            except Token.DoesNotExist:
                token = Token.objects.create(user=account)
            try:
                student = Student.objects.get(user = account)
                context['fees_paid'] = student.fees_paid
                context['application_submitted'] = student.application_submitted
                context['role'] = 'student'

            except:
                context['role'] = 'admin'
            context['response'] = 'Successfully authenticated.'
            context['pk'] = account.pk
            context['username'] = username.lower()
            context['token'] = token.key
        else:
            context['response'] = 'Error'
            context['error_message'] = 'Invalid credentials'
        return Response(context)

class LogoutView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self,request):
        context = {}
        try:
            request.user.auth_token.delete()
            # logout(request)
            context['response'] = 'Logout Successful.'
            status_code=status.HTTP_200_OK
        except:
            context['response'] = 'Error'
            context['error_message'] = 'Invalid Token'
            status_code=status.HTTP_400_BAD_REQUEST
        
        return Response(context,status=status_code)

class StudentRegisterView(APIView):
    serializer_class = AccountSerializer
    authentication_classes = []
    permission_classes = []

    def post(self,request):
        data = {}
        # print(request.data)
        email = request.data['email'].lower()
        if User.objects.filter(email = email,is_active=True).exists():
            data['error_message'] = 'That email is already in use.'
            data['response'] = 'Error'
            return Response(data)
        if User.objects.filter(username = request.data['username'],is_active=True).exists():
            data['error_message'] = 'That username is already in use.'
            data['response'] = 'Error'
            return Response(data)

        serializer = self.serializer_class(data=request.data)
        User.objects.filter(username =request.data['username'],is_active =False).delete()
        if serializer.is_valid():
            user = serializer.save()
            email = user.email
            otp = str(randint(100000, 999999))
            print("otp : ",otp)
            otp_verification = OtpVerification.objects.create(
                user=user,
                otp=otp
            )
            # request.session['otp'] = otp
            # print("sessionotp",request.session['otp'])
            # print("otp",otp)

            # request.session['email'] = email


            from_email = "careerportal.in <ecolumsmarketing@gmail.com>"
            subject = "Please Verify Your Email Address"
            text_content = "Dear <b>{}</b>,</br><p>We need to verify that {} is your email address so that it can be used with your career portal account.<br>OTP : <b>{}</b></p>".format(user.username,email,otp)
            try:
                msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
                msg.attach_alternative(text_content, "text/html")
                msg.send()
                print("Email send successfully")
            except:
                pass
            data['response'] = 'successfully registered new user.'
            data['email'] = user.email
            data['username'] = user.username
            data['otp_verification'] = otp_verification.id

            token = Token.objects.get(user=user).key
            # data['token'] = token
            student = Student.objects.create(user = user)
            # data['token'] = token
            # data['token'] = token
            status_code=status.HTTP_200_OK
        else:
            # print("error else")
            data = serializer.errors
        return Response(data,status=status.HTTP_200_OK)


class EmailVerification(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self,request):
        data = {}
        otp = request.data['otp']
        otp_verification = OtpVerification.objects.get(pk=request.data['otp_verification'])
        if (int(otp) == int(otp_verification.otp)):
            print("trueee")
            user = otp_verification.user
            user.is_active = True
            user.save()
            otp_verification.delete()
            data['response'] = "Email Verfied Successfully"
        else:
            if(otp_verification.count > 0):
                otp_verification.count -= 1
                otp_verification.save()
                data['response'] = "invalid OTP"
            else:
                otp_verification.delete()
                data['response'] = "Limit Exceeded, Register again !"
        return Response(data,status=status.HTTP_200_OK)
        

class ForgetPasswordEmail(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self,request):
        data={}
        email =request.data['email']
        if User.objects.filter(email=email).exists():
            otp = str(randint(100000, 999999))
            request.session['otp'] = otp
            request.session['email'] = email


            from_email = "careerportal.in <ecolumsmarketing@gmail.com>"
            subject = "One Time Password (OTP) for Forgot Password recovery on Career portal"
            text_content = "Dear <b>User</b>,</br><p>Your One Time Password (OTP) for Forgot Password recovery on Career portal is <b>{}</b>".format(otp)


            try:
                msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
                msg.attach_alternative(text_content, "text/html")
                msg.send()
                print("Email send successfully")
            except:
                pass
            data['response'] = "Your OTP for resetting Password has been sent to your email"
        else:
            data['response'] = "Account does not exist"

        return Response(data,status=status.HTTP_200_OK)

class ForgetPasswordVerification(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self,request):
        data = {}
        real_otp = int(request.session['otp'])
        otp = int(request.data['otp'])
        if (otp == real_otp):
            data['response'] = "Success"
        else:
            data['response'] = "Invalid OTP"
        return Response(data,status=status.HTTP_200_OK)
        

class ForgetPassword(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self,request):
        data = {}

        email = request.session['email']
        password = request.data['password']
        password2 = request.data['password2']

        if (password == password2):
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()

            data['response'] = "Password Changed succesfully"
        else:
            data['response'] = "Passwords must match"

        return Response(data,status=status.HTTP_200_OK)
        