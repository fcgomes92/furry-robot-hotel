from rest_framework.views import APIView
from rest_framework import status
from hotel_example import models, serializers, authentication
from hotel_example.renderer import JSONResponse


class UsersAPIView(APIView):
    http_methods = ['get', 'post', 'delete', ]
    content_type = 'application/json'

    authentication_classes = (authentication.PasswordAuthentication,)
    permission_classes = (authentication.IsAuthenticated,)

    def get(self, request, user_id=None, user_email=None, *args, **kwargs):
        if user_email:
            serializer = serializers.UserSerializer(
                models.User.objects.get(email=user_email))
        elif user_id:
            try:
                serializer = serializers.UserSerializer(
                    models.User.objects.get(id=user_id))
            except models.User.DoesNotExist:
                return None
        else:
            users = [user for user in models.User.objects.all()]
            serializer = serializers.UserSerializer(users, many=True)
        return JSONResponse.http_json_response(serializer.data)


class ProfileAPIView(APIView):
    http_methods = ['get', 'post', 'delete', ]
    content_type = 'application/json'

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (authentication.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = serializers.UserSerializer(request.user)
        return JSONResponse.http_json_response(serializer.data)
