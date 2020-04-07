from django.conf.urls import url
from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required

app_name='account'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('user_center/info/', login_required(views.UserInfoView.as_view()), name='info'),
    path('user_center/order/', login_required(views.UserOrderView.as_view()), name='userorder'),
    # path('login/get_valid_img/', views.get_valid_img, name='get_valid_img'),
]
