from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.exceptions import ParseError

User = get_user_model()

class RegistrationSerilalizer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
           'id', 'email', 'password', 'first_name', 'last_name'
        )

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise ParseError(
                'Пользователь с такой электронной почтой уже зарегистрирован'
            )
        return email
    
    def validate_password(self, value):
        validate_password(value)
        return value