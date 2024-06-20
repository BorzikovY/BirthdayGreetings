from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import (
    mixins,
    views, 
    viewsets, 
    status, 
    permissions
)

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from logic.models import User
from api.serializers import UserSerializer


class UserRegistrationView(views.APIView):

    permission_classes = [
        permissions.AllowAny
    ]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'full_name': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_EMAIL
                ),
                'birth_date': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_DATE,
                ),
            },
        )
    )
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(
    viewsets.GenericViewSet, 
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin
    ):
    permission_classes = ()
    queryset = User.objects.all()
    serializer_class = UserSerializer
