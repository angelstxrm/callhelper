from rest_framework import serializers

from users.models.profile import Profile


class ProfileShortSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'telegram_id',
        )

class ProfileUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'telegram_id',
        )