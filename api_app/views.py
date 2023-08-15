from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from django.contrib.auth import authenticate
from .renderers import UserDefineJsonRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Create your views here.

# jwt authentication

# manually token generate 

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
  renderer_classes = [UserDefineJsonRenderer]
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token':token,'msg':'Registration Success'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Another method 

# class UserRegistrationView(APIView):
#   renderer_classes = [UserDefineJsonRenderer]
#   def post(self, request, format=None):
#     serializer = UserRegistrationSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     user = serializer.save()
#     token = get_tokens_for_user(user)
#     return Response({'token':token,'msg':'Registration Success'}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
  renderer_classes = [UserDefineJsonRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
          token = get_tokens_for_user(user)
          return Response({'token':token,'msg':'Login Success'}, status=status.HTTP_200_OK)
    return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
  renderer_classes = [UserDefineJsonRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)



class PasswordChangeView(APIView):
  renderer_classes = [UserDefineJsonRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = PasswordChangeSerializer(data=request.data, context={'user':request.user}) #context={'user':request.user} current user serializers theke get korte bebohar kora hoy
    if serializer.is_valid(raise_exception=True):
      return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetEmailSendView(APIView):
  renderer_classes = [UserDefineJsonRenderer]
  def post(self, request, format=None):
    serializer = PasswordResetEmailSendSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
  renderer_classes = [UserDefineJsonRenderer]
  def post(self, request, uid, token, format=None):
    serializer = PasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    if serializer.is_valid(raise_exception=True):
      return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# without  jwt

# class UserRegistrationView(APIView):
#   renderer_classes = [UserDefineJsonRenderer]
#   def post(self, request, format=None):
#     serializer = UserRegistrationSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         user = serializer.save()
#         return Response({'msg':'Registration Success'}, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class UserLoginView(APIView):
#   renderer_classes = [UserDefineJsonRenderer]
#   def post(self, request, format=None):
#     serializer = UserLoginSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         email = serializer.data.get('email')
#         password = serializer.data.get('password')
#         user = authenticate(email=email, password=password)
#         if user is not None:
#           return Response({'msg':'Login Success'}, status=status.HTTP_200_OK)
#     return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
