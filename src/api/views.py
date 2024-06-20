from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import (
    mixins,
    views, 
    viewsets, 
    status, 
    permissions,
)

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from logic.models import User, Subscription
from api.serializers import (
    UserRegisterSerializer,
    UserSerializer,
    SubscriptionSerializer,
)


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
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Пользователь успешно создан."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


class UserViewSet(
        viewsets.GenericViewSet, 
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin
    ):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def destroy(self, request: Request, pk=None) -> Response:
        """Удаляет аккаунт пользователя."""
        user = self.get_object()
        if user == request.user:
            user.delete()
            return Response(
                {'message': 'Аккаунт успешно удален.'},
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            return Response({'detail': 'Недостаточно прав.'}, status=status.HTTP_403_FORBIDDEN)

class SubscriptionViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    ):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return Subscription.objects.filter(subscriber=self.request.user)    

    # def retrieve(self, request, *args, **kwargs):
    #     return super().retrieve(request, *args, **kwargs)