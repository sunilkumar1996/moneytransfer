from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

User = get_user_model()


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# Register Serializer class 
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, 
        validators=[UniqueValidator(queryset=User.objects.all())]
        )

    password = serializers.CharField(
        write_only=True, 
        required=True
        )
    password2 = serializers.CharField(
        write_only=True,
        required=True
        )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "dob", "country", "city", "state", "postal_code", "email", "password", "password2", ]
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "dob": {"required": True},
            "country": {"required": True},
            "city": {"required": True},
            "state": {"required": True},
            "postal_code": {"required": True},
            "email": {"required": True},
            }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match!!"})
        return attrs

    def create(self, validated_data):
        # first_name = validated_data["fist_name"]
        # last_name = validated_data["last_name"]
        # dob = validated_data["dob"]
        # country = validated_data["country"]
        # city = validated_data["city"]
        # state = validated_data["state"]
        # postal_code = validated_data["postal_code"]
        # email = validated_data["email"]
        # password = validated_data["password"]
        # password2 = validated_data["password2"]
        # # if (email and User.objects.filter(email=email).exclude(username=username).exists()):
        # if (email and User.objects.filter(email=email).exists()):
        #     raise serializers.ValidationError(
        #         {"email": "Email addresses must be unique."})
        # if password != password2:
        #     raise serializers.ValidationError(
        #         {"password": "The two passwords differ."})
        user = User.objects.create(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            dob = validated_data['dob'],
            country = validated_data['country'],
            city = validated_data['city'],
            state = validated_data['state'],
            postal_code = validated_data['postal_code'],
            email = validated_data['email'],
            password = make_password(validated_data['password'])
        )
        # user.set_password(validate_password['password'])
        user.save()
        return user