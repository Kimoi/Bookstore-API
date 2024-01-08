from datetime import datetime
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.models import Book, OrderItem, Order, Shop, Cart


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "release_date"]

    def create(self, validated_data):
        book = Book.objects.create(
            title=validated_data["title"],
            author=validated_data["author"],
            release_date=validated_data["release_date"]
        )
        book.save()
        return book


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ["id", "name", "address"]


class CartSerializer(serializers.ModelSerializer):
    book = serializers.CharField(source="book.title", read_only=True)
    user = serializers.CharField(source="user.username", read_only=True)
    quantity = serializers.IntegerField(min_value=1, max_value=10, required=True)
    shop = serializers.CharField(source="shop.name", read_only=True)
    book_item = serializers.CharField(write_only=True)
    shop_item = serializers.CharField(write_only=True)

    class Meta:
        model = Cart
        fields = ["id", "book", "user", "quantity", "shop", "book_item", "shop_item"]

    def create(self, validated_data):
        user = User.objects.get(id=self.context["request"].user.id)
        book = get_object_or_404(Book, title=validated_data["book_item"])
        shop = get_object_or_404(Shop, name=validated_data["shop_item"])
        cart = Cart.objects.create(
            user=user,
            book=book,
            quantity=validated_data["quantity"],
            shop=shop
        )
        cart.save()
        return cart


class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.CharField(source="order.id", read_only=True)
    book = serializers.CharField(source="book.title", read_only=True)
    shop = serializers.CharField(source="shop.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "order", "book", "quantity", "shop"]
        read_only_fields = ["id", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    books = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "user", "date", "books"]
        read_only_fields = ["id", "date"]

    def get_books(self, order: Order):
        queryset = order.items.filter(order=order)
        return OrderItemSerializer(queryset, many=True).data

    def create(self, validated_data):
        user = User.objects.get(id=self.context["request"].user.id)
        cart = Cart.objects.filter(user=user)
        if not cart:
            raise serializers.ValidationError(f"{user.username} have no books in cart")
        order = Order.objects.create(
            user=user,
            date=datetime.now()
        )
        order.save()

        for book in cart:
            item = OrderItem.objects.create(
                order=order,
                book=book.book,
                quantity=book.quantity,
                shop=book.shop
            )
            item.save()
        cart.delete()
        order.save()
        return order
