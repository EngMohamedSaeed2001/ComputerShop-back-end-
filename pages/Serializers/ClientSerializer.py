from rest_framework import serializers

from pages.models import Client, Favourite, Order


# Client Serializer

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


# fav serializer

class AddFavSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = "__all__"

    def create(self, validated_data):
        fav = Favourite(product=validated_data['product'])
        fav.save()
        return fav


class FavSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = "__all__"


# order serializer

class AddOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'product', 'address']

    def create(self, validated_data):
        order = Order(product=validated_data['product'], address=validated_data['address'])
        order.save()
        return order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'product', 'address']
