from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer

class UserRegistrationView(views.APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(views.APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response({'message': 'User logged in successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
def home(request):
    return HttpResponse("Welcome to My Project API!")