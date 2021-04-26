import os

from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated


User = get_user_model()


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


# @api_view(['POST', 'GET'])
# @permission_classes([permissions.AllowAny])
# def register(request):
#     serializer = UserCreateSerializer(data=request.data)
#     print("Serializer :", serializer)
#     if not serializer.is_valid():
#         res = {
#             "email": "This field is required.",
#             "Passowrd": "This field is required.",
#         }
#         return Response(res, status=status.HTTP_400_BAD_REQUEST)

#     user = serializer.save()
#     print("it is working.")
#     refresh = RefreshToken.for_user(user)
#     res = {
#         "refresh": str(refresh),
#         "accress": str(refresh.access_token)
#     }
#     return Response(res, status.HTTP_201_CREATED)


# @api_view(['POST'])
# @permission_classes([])