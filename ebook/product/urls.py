from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from . import views
app_name='[product]'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('product_list/<int:category_pk>/', views.product_list, name='product_list'),
    path('product_detail/<int:product_pk>/',views.product_detail, name='product_detail'),

    ]