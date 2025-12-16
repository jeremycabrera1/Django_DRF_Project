from inventory.models import Category, Product, PromotionEvent, StockManagement
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


class StockManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockManagement
        fields = ["quantity"]


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


class CreateProductStockSerializer(serializers.ModelSerializer):
    stock_data = StockManagementSerializer(required=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "is_digital",
            "is_active",
            "price",
            "category",
            "stock_data",
        ]

    def create(self, validated_data):
        stock_data = validated_data.pop("stock_data", None)

        product = Product.objects.create(**validated_data)
        StockManagement.objects.create(product=product, **stock_data)

        return product