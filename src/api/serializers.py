from rest_framework import serializers
from logic.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        email = validated_data.get('email')

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
        )

        return user