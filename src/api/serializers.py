from rest_framework import serializers
from logic.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email') # Adjust fields as needed

    def create(self, validated_data):
        # Extract data for the fields you're creating
        username = validated_data.get('username')
        password = validated_data.get('password')
        email = validated_data.get('email')

        # Create the user instance
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
        )

        return user