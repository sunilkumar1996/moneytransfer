from django.urls import include, path
# from rest_framework import routers
from . import views
from django.contrib.auth import views as auth_views
from .views import RegisterView, LogoutAPIView, LoginApiKnox, SetNewPasswordAPIView, VerifyEmail, LoginAPIView, PasswordTokenCheckAPI, RequestPasswordResetEmail, ChangePasswordView
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenObtainPairView
)

from rest_auth.views import PasswordResetConfirmView, PasswordResetView
from knox import views as knox_views
from django.contrib.auth import views as pass_reset_views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from .helpers import LogoutAllUserView, LogoutUserView

schema_view = get_schema_view(
    openapi.Info(
        title="Swiftyre API",
        default_version="v1",
        description="The internal API used by Swiftyre",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [

    path('swager/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/api.json/', schema_view.without_ui(cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('auth/login/', LoginApiKnox.as_view(), name='knoz_login'),
    path('auth/register/', RegisterView.as_view(), name="register"),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('rest_auth/', include('rest_auth.urls')),
    # path('login/', LoginAPIView.as_view(), name="login"),
    # path('auth/token/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('rest-auth/password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('api/logout/', LogoutUserView.as_view(), name='logout'),
    path('api/logoutall/', LogoutAllUserView.as_view(), name='logoutall'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change-password'),
    # path('password_reset/', pass_reset_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', pass_reset_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', pass_reset_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html", ), name='password_reset_confirm'),
    path('reset/done/', pass_reset_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html', ), name='password_reset_complete'),
    path('update/profile/', views.UpdateProfileView.as_view(), name='update_profile'),
]
