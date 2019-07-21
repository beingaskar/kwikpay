"""kwikpay URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # API to obtain token using `username` and `password`
    path('api/authenticate/', obtain_auth_token, name='obtain_token'),

    # Promotion related URL's
    path('api/promo/', include('promotions.urls')),

    # Account related URL's
    path('api/accounts/', include('accounts.urls')),

    # Wallet related URL's
    path('api/', include('wallet.urls')),

]

urlpatterns += staticfiles_urlpatterns()