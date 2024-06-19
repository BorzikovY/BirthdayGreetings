from rest_framework import views, status
from rest_framework import permissions
from rest_framework.response import Response
from api.serializers import UserSerializer


class UserRegistrationView(views.APIView):

    permission_classes = [
        permissions.AllowAny
    ]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
