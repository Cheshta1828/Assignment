from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer 
from rest_framework import permissions
from django.contrib.auth import login
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

from django.core.exceptions import PermissionDenied
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated   
from rest_framework.response import Response
from rest_framework import generics

from django.views.decorators.csrf import csrf_exempt

specialCharacters="!@#$%^&*?//"

# Register API
from django.core.files import File

from django.core.files import File

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        
        validated_data = serializer.validated_data

       
        
        password = validated_data['password']
        if len(password) <8:
             return Response({"error": "password should be greater than 8 characters"}, status=status.HTTP_400_BAD_REQUEST)
        elif(any(char.isalpha() for char in password) == False):
            return Response({"error": "password should contain atleast 1 alphabet"}, status=status.HTTP_400_BAD_REQUEST)
        elif(any(char.isupper() for char in password) == False):
            return Response({"error": "password should contain atleast 1 uppercase letter"}, status=status.HTTP_400_BAD_REQUEST)
        elif(any(char.islower() for char in password) == False):
            return Response({"error": "password should contain atleast 1 lowercase letter"}, status=status.HTTP_400_BAD_REQUEST)
        elif(any(char.isdigit() for char in password) == False):
            return Response({"error": "password should contain atleast 1 digit"}, status=status.HTTP_400_BAD_REQUEST)
        elif all(x not in specialCharacters for x in password):
            return Response({"error": "password should contain atleast 1 special character"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        

        token = default_token_generator.make_token(user)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })



#Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
       
        
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)






@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getprofile(request):
   user = request.user
   serializer = UserSerializer(user)
   return Response({
        "username": serializer.data['username'],
        "email": serializer.data['email']
    })




@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def updateprofile(request):
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)

    serializer.is_valid(raise_exception=True)
    print(serializer.validated_data)

    

    serializer.save()
    return Response({'msg': 'Updated your profile.'})


