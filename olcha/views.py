from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import (
    Category, Product, ProductImage, Comment,
    Attribute, AttributeKey, AttributeValue
)
from .serializers import (
    CategorySerializer, ProductSerializer, ProductImageSerializer,
    CommentSerializer, AttributeSerializer, AttributeKeySerializer,
    AttributeValueSerializer
)
from .permissions import IsOwnerOrReadOnly
from .pagination import Pagination





class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.prefetch_related('products')
    serializer_class = CategorySerializer



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').prefetch_related(
        'comments',
        'images',
        'attributes__attribute_key',
        'attributes__attribute_value',
    )
    serializer_class = ProductSerializer
    pagination_class = Pagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'category__title']

    @method_decorator(cache_page(60 * 5))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.select_related('product')
    serializer_class = ProductImageSerializer
    pagination_class = Pagination



class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.select_related(
        'product', 'attribute_key', 'attribute_value'
    )
    serializer_class = AttributeSerializer
    pagination_class = Pagination



class AttributeKeyViewSet(viewsets.ModelViewSet):
    queryset = AttributeKey.objects.prefetch_related('attribute_set')
    serializer_class = AttributeKeySerializer
    pagination_class = Pagination



class AttributeValueViewSet(viewsets.ModelViewSet):
    queryset = AttributeValue.objects.prefetch_related('attribute_set')
    serializer_class = AttributeValueSerializer
    pagination_class = Pagination


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('product', 'owner')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    pagination_class = Pagination