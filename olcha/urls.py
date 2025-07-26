app_name = 'olcha'

from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, ProductViewSet, ProductImageViewSet,
    CommentViewSet, AttributeViewSet, AttributeKeyViewSet, AttributeValueViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'images', ProductImageViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'attributes', AttributeViewSet)
router.register(r'attribute-keys', AttributeKeyViewSet)
router.register(r'attribute-values', AttributeValueViewSet)

urlpatterns = router.urls