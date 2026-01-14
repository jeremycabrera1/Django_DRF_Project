from inventory.models import (
    Category,
    Order,
    Product,
    StockManagement,
    User,
    OrderProduct,
)
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "parent", "name", "slug", "level", "is_active"]


class CategoryReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class StockManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockManagement
        fields = ["quantity"]


class CreateProductSerializer(serializers.ModelSerializer):
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
        ]


class CreateProductStockSerializer(serializers.ModelSerializer):
    stock_data = StockManagementSerializer(write_only=True, required=True)

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

    def to_representation(self, instance):
        """Customize the representation to include stock data."""
        # Start with the default representation
        data = super().to_representation(instance)

        # Fetch the related stock data from the StockManagement model
        stock_instance = StockManagement.objects.filter(product=instance).first()

        # If stock data exists, add it to the response
        if stock_instance:
            data["stock_data"] = StockManagementSerializer(stock_instance).data
        else:
            data["stock_data"] = None  # In case there's no related stock data

        return data


class OrderProductSerializer(serializers.ModelSerializer):
    """Handles individual product entries within an order"""

    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderProduct
        fields = ["product", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    """Handles order creation with multiple products"""

    products = OrderProductSerializer(
        many=True, write_only=True
    )  # Accept a list of products

    class Meta:
        model = Order
        fields = ["user", "created_at", "updated_at", "products"]

    def create(self, validated_data):
        products_data = validated_data.pop("products")  # Extract product list
        order = Order.objects.create(**validated_data)  # Create the order

        # Create OrderProduct entries for each product in the request
        order_products = [
            OrderProduct(order=order, **product_data) for product_data in products_data
        ]
        OrderProduct.objects.bulk_create(order_products)  # Bulk insert

        return order

class CategoryBulkDeleteSerializer(serializers.Serializer):
    ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        help_text="List of category IDs to delete",
    )