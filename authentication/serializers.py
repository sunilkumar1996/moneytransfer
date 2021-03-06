from rest_framework import serializers
# from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError, AccessToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class AuthTokenLoginSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Username"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    class Meta:
        model = User
        fields = [
            "first_name", 
            "last_name", 
            "dob", 
            "phone_number", 
            "country", 
            "city", 
            "state", 
            "postal_code", 
            "email", 
            "password", 
            "password2", 
            "account_type", 
            "image_url",
            "is_verified",
            ]

    def validate(self, attrs):
        username = attrs.get('email')
        password = attrs.get('password')

        if username and password:
            obj = User.objects.filter(email=username).first()
            if obj:
                if obj.is_active == False:
                    raise serializers.ValidationError({"message": "Your Email is not confirm !!"})
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    """
    Serializer For Password change Endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UpdateUserSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(required=True)
    # first_name = serializers.CharField(required=True)
    # last_name = serializers.CharField(required=True)
    # dob = serializers.DateField(required=True)
    # phone_number = serializers.CharField(required=True)
    # country = serializers.CharField(required=True)
    # city = serializers.CharField(required=True)
    # state = serializers.CharField(required=True)
    # postal_code = serializers.IntegerField(required=True)
    image_url = serializers.ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = User
        fields = [
            "first_name", 
            "last_name", 
            "dob", 
            "phone_number", 
            "country", 
            "city", 
            "state", 
            "postal_code", 
            "email", 
            "account_type",
            "image_url",
            ]

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email',instance.email)
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.dob = validated_data.get('dob',instance.dob)
        instance.phone_number = validated_data.get('phone_number',instance.phone_number)
        instance.country = validated_data.get('country',instance.country)
        instance.city = validated_data.get('city',instance.city)
        instance.state = validated_data.get('state',instance.state)
        instance.postal_code = validated_data.get('postal_code',instance.postal_code)
        instance.account_type = validated_data.get('account_type',instance.account_type)
        instance.image_url = validated_data.get('image_url', instance.image_url)
        print("Image Url : ", instance.image_url)
        instance.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):

    # email = serializers.EmailField(
    #     required=True, 
    #     validators=[UniqueValidator(queryset=User.objects.all())]
    #     )

    password = serializers.CharField(
        write_only=True,
        required=True
        )

    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        model = User
        fields = [
            "first_name", 
            "last_name", 
            "dob", 
            "phone_number", 
            "country", 
            "city", 
            "state", 
            "postal_code", 
            "email", 
            "password", 
            "password2", 
            "account_type", 
            "image_url",
            "is_verified",
            ]

    def validate(self, attrs):
        email = attrs.get('email', '')
        phone_number = attrs.get('phone_number', '')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "This Email is already exists!!"})

        if User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError({"Phone_Number": "This Phone Number is already exists!!"})

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match !!"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            dob = validated_data['dob'],
            phone_number = validated_data['phone_number'],
            country = validated_data['country'],
            city = validated_data['city'],
            state = validated_data['state'],
            postal_code = validated_data['postal_code'],
            email = validated_data['email'],
            account_type = validated_data['account_type'],
            password = make_password(validated_data['password'])
        )
        user.save()
        return user


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(max_length=255, min_length=3)
    # password = serializers.CharField(
    #     max_length=68, min_length=4, write_only=True)
    # username = serializers.CharField(
    #     max_length=255, min_length=3, read_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': RefreshToken,
            'access': AccessToken
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        print(filtered_user_by_email)
        user = authenticate(email=email, password=password)

        # if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
        #     raise AuthenticationFailed(
        #         detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')

        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            # 'username': user.username,
            # 'tokens': user.tokens
        }

        return super().validate(attrs)


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')
