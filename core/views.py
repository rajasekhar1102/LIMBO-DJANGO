
from rest_framework.response import Response
from rest_framework import status
from djoser.views import UserViewSet as BaseUserViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
import json


User = get_user_model()


class UserViewSet(BaseUserViewSet):

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user = User.objects.get(email=serializer.data['email'])
        user_tokens = RefreshToken.for_user(user)
        user_tokens['username'] = user.username
        user_tokens['email'] = user.email
        tokens = {'refresh': str(user_tokens),
                  'access': str(user_tokens.access_token)}

        headers['x-auth-token'] = json.dumps(tokens)
        headers['access-control-expose-headers'] = 'x-auth-token'
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
