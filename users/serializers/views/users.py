# import pdb
from django.contrib.auth import get_user_model

from drf_spectacular.utils import extend_schema_view, extend_schema

from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from users.serializers.api import users as user_s

User = get_user_model()


@extend_schema_view(
    post=extend_schema(summary='Регистрация пользователя', tags=['Аутентификация & Авторизация']),
)

class RegistrationView(CreateAPIView):
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