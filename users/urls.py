from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, CustomObtainPairView, LogoutView, UserViewSet
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'users'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
