"""computerShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from pages.views import SignUp, Logout, ResetPassword

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('pages.urls', 'computerShop'), namespace='computerShop')),
    path('api-token/', views.obtain_auth_token, name='api-auth-token'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ////////Registeration////////

    path('auth/signup/', SignUp.as_view(), name='signup'),
    # path('auth/email_verify/', VerifyEmail.as_view(), name='email_verify'),
    path('auth/reset-password/', ResetPassword.as_view(), name='reset-password'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/logout/', Logout.as_view(), name="logout"),

    # path('computerShop/logout/', knox_views.LogoutView.as_view(), name='logout'),
    # path('computerShop/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),

]
