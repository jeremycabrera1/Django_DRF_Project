from drf_spectacular.utils import extend_schema
from inventory.models import Category
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .serializers import (
    CategoryReturnSerializer,
    CategorySerializer,
    CreateProductSerializer,
)

# Create your views here.


# class InventoryCategoryModelViewSet(ModelViewSet):
#     queryset = Category.objects.all() # Fetch all categories
#     serializer_class = InventoryCategorySerializer # Use the serializer


# class InventoryCategoryViewSet(ViewSet):
#     def list(self, request):
#         queryset = Category.objects.all()
#         serializer = InventoryCategorySerializer(queryset, many=True)
#         return Response(serializer.data)


# class InventoryCategoryModelViewSet(ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = InventoryCategorySerializer


class CategoryInsertViewSet(ViewSet):
    @extend_schema(
        request=CategorySerializer,
        responses={201: CategoryReturnSerializer},
        tags=["Module 4"],
    )
    def create(self, request):
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            category_instance = serializer.save()
            return_serializer = CategoryReturnSerializer(category_instance)
            return Response(return_serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryBulkInsertViewSet(ViewSet):
    @extend_schema(
        request=CategorySerializer(many=True),
        responses={201: CategorySerializer(many=True)},
        tags=["Module 4"],
    )
    def create(self, request):
        # Ensure the request contains a list of items
        if not isinstance(request.data, list):
            return Response(
                {"error": "Expected a list of objects"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Deserialize data (many=True allows multiple objects)
        serializer = CategorySerializer(data=request.data, many=True)

        if serializer.is_valid():
            # Convert validated data to model instances (without saving yet)
            categories = [Category(**item) for item in serializer.validated_data]
            # Use bulk_create() to insert all at once
            created_categories = Category.objects.bulk_create(categories)
            # Serialize the created objects and return response
            return Response(
                CategorySerializer(created_categories, many=True).data,
                status=status.HTTP_201_CREATED,
            )

        else:
            # Return validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryUpdateWithSaveViewSet(ViewSet):
    queryset = Category.objects.all()

    @extend_schema(
        request=CategorySerializer,  # Request body structure
        responses={200: CategorySerializer},  # Expected response format
        tags=["Module 4"],
    )
    def update(self, request, pk: int):  # 'pk' is the primary key of the object
        try:
            category = Category.objects.get(pk=pk)  # Fetch the existing record
        except Category.DoesNotExist:
            return Response(
                {"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CategorySerializer(category, data=request.data)  # Validate data

        if serializer.is_valid():
            serializer.save()  # Update the record
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryPartialUpdateWithSaveViewSet(ViewSet):
    queryset = Category.objects.all()

    @extend_schema(
        request=CategorySerializer,  # Request body structure
        responses={200: CategorySerializer},  # Expected response format
        tags=["Module 4"],
    )
    def partial_update(self, request, pk: int):  # 'pk' is the primary key of the object
        try:
            category = Category.objects.get(pk=pk)  # Fetch the existing record
        except Category.DoesNotExist:
            return Response(
                {"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CategorySerializer(
            category, data=request.data, partial=True
        )  # Validate data

        if serializer.is_valid():
            serializer.save()  # Update the record
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductInsertView(ViewSet):
    @extend_schema(
        request=CreateProductSerializer,
        responses={201: CreateProductSerializer},
        tags=["Module 4"],
    )
    def create(self, request):
        """
        Creates a Product
        """

        serializer = CreateProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
