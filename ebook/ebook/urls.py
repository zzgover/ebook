"""ebook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls.static import static   # 新加入
from django.conf import settings             # 新加入

urlpatterns = [
    path('admin/', admin.site.urls),
    path('order/', include('order.urls',namespace='order')),
    path('cart/',include('cart.urls',namespace='cart')),
    path('account/',include('account.urls',namespace='account')),
    path('',include('product.urls',namespace='product')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 新加入
