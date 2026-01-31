from drf_spectacular.utils import (
    extend_schema,
)
from inventory.models import Category
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .serializers import (
    CategorySerializer,
)


@extend_schema(
    tags = ['Module 5']
)

class CategoryListViewSet(ViewSet):
    '''
    Retrieves all categories with full model objects
    '''

    def list(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)