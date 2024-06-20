from rest_framework import serializers
from logic.models import User, Subscription


class UserRegisterSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = User
        fields = ('id', 'full_name', 'email', 'birth_date',) 
        read_only_fields = ('id',)   


class SubscriptionSerializer(serializers.ModelSerializer):
    birthday_person = UserSerializer()

    class Meta:
        model = Subscription
        fields = ('birthday_person', 'notification_time',)
