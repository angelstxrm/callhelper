# import pdb
from django.contrib.auth import get_user_model

from drf_spectacular.utils import extend_schema_view, extend_schema

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from users.serializers.api import users as user_s

User = get_user_model()


@extend_schema_view(
    post=extend_schema(summary='Регистрация пользователя', tags=['Аутентификация & Авторизация']),
)

class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = user_s.RegistrationSerializers

@extend_schema_view(
    post=extend_schema(
        request=user_s.ChangePasswordSerializers,
        summary='Смена пароля', tags=['Аутентификация & Авторизация']
    ),
)

class ChangePasswordView(APIView):

    def post(self, request):
        user = request.user
        serializer = user_s.ChangePasswordSerializers(
            instance=user, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_204_NO_CONTENT)

@extend_schema_view(
    get=extend_schema(
        summary='Профиль пользователя', tags=['Пользователи']
    ),
    put=extend_schema(
        summary='Изменить профиль пользователя', tags=['Пользователи']
    ),
    patch=extend_schema(
        summary='Изменить частично профиль пользователя', tags=['Пользователи']
    ),
)

class MeView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = user_s.MeListSerializers
    http_method_names = ('get', 'patch')

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return user_s.MeUpdateSerializers
        return user_s.MeListSerializers

    def get_object(self):
        return self.request.user