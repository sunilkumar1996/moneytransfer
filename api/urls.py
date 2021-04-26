from django.urls import include, path
from rest_framework import routers
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('auth/', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/token/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', views.RegisterView.as_view(), name='register'),
]