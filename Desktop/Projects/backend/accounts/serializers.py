from rest_framework import serializers
from django.contrib.auth import password_validation as pv

from .models import User, Admin


class AdminRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(max_length=64, write_only=True)
    password2 = serializers.CharField(max_length=64, write_only=True)

    class Meta:
        model = Admin
        fields = "__all__"
        read_only_fields = ['user',  ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('Пароль не совпадают')
        return attrs

    def validate_password(self, value):
        try:
            pv.validate_password(value)
        except pv.ValidationError as e:
            raise serializers.ValidationError(e)
        else:
            return value

    def create(self, validated_data):
        try:
            user = User(username=validated_data['username'], email=validated_data['email'])
            user.set_password(validated_data['password'])
            user.save()
        except Exception as e:
            raise serializers.ValidationError(f'Не удалось создать пользователя {e}')
        else:
            admin = Admin.objects.create(
                is_admin=validated_data['is_admin'],
                user=user,
                email=validated_data['email']
            )
            return admin


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', ]
        read_only_fields = ['is_admin', ]
