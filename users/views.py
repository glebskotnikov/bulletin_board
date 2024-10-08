from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (PasswordResetConfirmSerializer,
                          PasswordResetSerializer, UserRegisterSerializer)


class RegisterUserView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "user": serializer.data,
                    "message": "User created successfully",
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Password reset e-mail sent"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Password has been reset with the new password."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
