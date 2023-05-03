from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .models import User, Admin
from .serializers import AdminRegisterSerializer, UserSerializer
from tests.permissions import AdminPermission


class AdminRegisterListCreateAPIView(generics.ListCreateAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminRegisterSerializer

    def create_admin(self, request, is_admin):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(is_admin=is_admin)
            token, created = Token.objects.get_or_create(user=request.user)
            return Response({'token': token.key}, serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminPermission]
