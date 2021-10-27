from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from pages.models import Client, Product, Section, Offer


# User Serializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters',
    }

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages['username'])

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        client = Client(username=user.username, password=user.password, email=user.email)
        client.save()
        return user


# verify account serializer

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


# LogOut serializer
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            error_message = 'Token is expired or invalid'
            return error_message


# Section Serializer


class SectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = "__all__"


class AddSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = "__all__"

    def create(self, validated_data):
        section = Section(name=validated_data['name'], image=validated_data['image'])
        section.save()
        return section


# Product Serializer

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class AddProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'price', 'section')

    def create(self, validated_data):
        product = Product(name=validated_data['name'], description=validated_data['description'],
                          image=validated_data['image'],
                          price=validated_data['price'], section=validated_data['section'])
        product.save()
        return product


# Offer Serializer

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = "__all__"


class AddOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = "__all__"

    def create(self, validated_data):
        offer = Offer(product=validated_data['product'],
                      date=validated_data['date'],
                      offer=validated_data['offer'])
        offer.save()
        return offer
