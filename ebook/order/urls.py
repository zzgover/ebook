from django.conf.urls import url, include
from django.urls import path

from . import views
from django.contrib.auth.decorators import login_required
app_name='[order]'
urlpatterns = [
    path('order_create/', login_required(views.OrderCreateView.as_view()), name='order_create'),
    path('order_created/', login_required(views.OrderCreatedView.as_view()), name='order_created'),
    path('pay/<int:order_id>/', login_required(views.OrderPayView.as_view()),name='pay'),
    # 支付宝完成支付后的返回页面
    path('return_pay/', views.return_pay, name='return_pay'),
]
