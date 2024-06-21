from rest_framework import serializers
from logic.models import User, Subscription


class UserRegisterSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя при регистрации."""
    class Meta:
        model = User
        fields = (
            'id', 
            'full_name', 
            'password', 
            'email', 
            'birth_date',
        )

    def create(self, validated_data):
        """Создает пользователя."""
        full_name = validated_data.get('full_name')
        password = validated_data.get('password')
        email = validated_data.get('email')
        birth_date = validated_data.get('birth_date')

        user = User.objects.create_user(
            full_name=full_name,
            password=password,
            email=email,
            birth_date=birth_date
        )

        return user


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""
    class Meta:
        model = User
        fields = ('id', 'full_name', 'email', 'birth_date',) 
        read_only_fields = ('id',)   


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки."""
    birthday_person = UserSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = ('id', 'birthday_person', 'notification_time',)


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания подписки."""
    birthday_person_id = serializers.IntegerField(
        source='birthday_person.id',
        required=True,
    )

    class Meta:
        model = Subscription
        fields = ['id', 'birthday_person_id', 'notification_time']

    def create(self, validated_data):
        """
        Создает подписку.
        """
        birthday_person_id = validated_data.pop('birthday_person')['id']
        birthday_person = User.objects.get(id=birthday_person_id)
        validated_data['birthday_person'] = birthday_person
        validated_data['subscriber'] = self.context['request'].user
        return super().create(validated_data)


class UpdateNotificationTimeSerializer(serializers.ModelSerializer):
    """Сериализатор изменения времени отправки напоминания,"""
    class Meta:
        model = Subscription
        fields = ['notification_time']
    