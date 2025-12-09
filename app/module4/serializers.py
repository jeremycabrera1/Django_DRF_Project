from inventory.models import Category, Product, PromotionEvent
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "parent", "name", "slug", "is_active", "level"]


class CategoryReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class PromotionEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionEvent
        fields = ["id", "name", "price_reduction", "start_date", "end_date"]


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "name",
            "slug",
            "description",
            "is_digital",
            "is_active",
            "created_at",
            "updated_at",
            "price",
        ]
