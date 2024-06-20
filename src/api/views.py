from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
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
    SubscriptionCreateSerializer,
    UpdateNotificationTimeSerializer,
)


class UserRegistrationView(views.APIView):

    permission_classes = [permissions.AllowAny]

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
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request: Request, pk=None, *args, **kwargs) -> Response:
        """Обновляет данные пользователя, если запрос отправлен авторизованным пользователем."""
        if pk == str(request.user.pk) and User.objects.get(id=pk):
            return super().update(request, *args, **kwargs)
        return Response({"detail": "Недостаточно прав."}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request: Request, pk=None) -> Response:
        """Удаляет аккаунт пользователя."""
        user = self.get_object()
        if user == request.user:
            user.delete()
            return Response(
                {'detail': 'Аккаунт успешно удален.'},
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            return Response({'detail': 'Недостаточно прав.'}, status=status.HTTP_403_FORBIDDEN)


class SubscriptionViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    ):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Получаем подписки только для указанного подписчика
        """
        return Subscription.objects.filter(subscriber=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubscriptionCreateSerializer
        elif self.request.method == 'PUT':
            return UpdateNotificationTimeSerializer
        return SubscriptionSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        if user := User.objects.filter(id=serializer.validated_data['birthday_person']['id']).first():
            if not Subscription.objects.filter(subscriber=self.request.user, birthday_person=user):
                serializer.validated_data['subscriber'] = request.user
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(
                {'detail': 'Вы уже подписаны на этого пользователя'},
                status=status.HTTP_403_FORBIDDEN
            )
        return Response(
            {'detail': 'Пользователь с таким id не существует'},
            status=status.HTTP_403_FORBIDDEN
        )
    @action(detail=True, methods=['PUT'], url_path='notification-time')
    def update_notification_time(self, request, pk=None):
        subscription = self.get_object()
        serializer = UpdateNotificationTimeSerializer(
            subscription, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, birthday_person_pk=None, pk=None):
        """
        Удаляем подписку
        """
        subscription = self.get_object()
        if subscription.subscriber != request.user:
            return Response({"detail": "Недостаточно прав для удаления"}, status=403)

        subscription.delete()

        return Response(status=204)
