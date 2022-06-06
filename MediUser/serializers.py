from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import serializers

from MediUser.models import MediUser


class MediRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediUser
        fields = ['username', 'password', 'mobile', 'email', 'profile_image']

        username = serializers.CharField(
            label="Username",
            write_only=True
        )
        password = serializers.CharField(
            label="Password",
            # This will be used when the DRF browsable API is enabled
            style={'input_type': 'password'},
            trim_whitespace=False,
            write_only=True
        )
        mobile = serializers.IntegerField(
            label="mobile",
            style={'input_type': 'number'},
            write_only=True
        )
        email = serializers.EmailField(
            label="email",
            style={'input_type': 'email'},
            write_only=True
        )
        profile_image = serializers.ImageField(
            label="profile-image",
            style={'input_type': 'image'},
            write_only=True
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()

        user1 = MediUser()
        user1.username = validated_data['username']
        user1.password = validated_data['password']
        user1.mobile = validated_data['mobile']
        user1.email = validated_data['email']

        # user1.profile_image = validated_data['profile_image']

        user1.user = User.objects.get(username=validated_data['username'])

        user1.save()
        print(user1.profile_image)
        return user1


class MediLoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

