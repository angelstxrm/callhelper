from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ParseError

from users.serializers.nested.profile import ProfileUpdateSerializers, ProfileShortSerializers

User = get_user_model()

class RegistrationSerializers(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

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
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ChangePasswordSerializers(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields = ('old_password', 'new_password')

    def validate(self, attrs):
        user = self.instance
        old_password = attrs.pop('old_password')
        if not user.check_password(old_password):
            raise ParseError(
                'Старый пароль введен неверно'
            )
        return attrs

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop('new_password')
        instance.set_password(password)
        instance.save()
        return instance
    
class MeListSerializers(serializers.ModelSerializer):
    profile = ProfileShortSerializers()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'username',
            'phone_number',
            'profile',
            'date_joined',
        )


class MeUpdateSerializers(serializers.ModelSerializer):
    profile = ProfileUpdateSerializers()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'username',
            'phone_number',
            'profile',
        )

    def update(self, instance, validated_data):
        # Проверка наличия профиля
        profile_data = validated_data.pop('profile') if 'profile' in validated_data else None

        with transaction.atomic():
            instance = super().update(instance, validated_data)
            self._update_profile(instance.profile, profile_data)

        return instance    

    def _update_profile(self, profile, data):
        profile_serializer = ProfileUpdateSerializers(
            instance=profile,
            data=data,
            partial=True,
        )
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()