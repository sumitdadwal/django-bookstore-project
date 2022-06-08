from django.urls import path
from .views import *

app_name = "ecomadmin"

urlpatterns = [
    path('login/', AdminLoginView.as_view(), name='adminlogin'),
    path('logout/', AdminLogoutView.as_view(), name='adminlogout'),
    path('register/', AdminRegistrationView.as_view(), name='adminregister'),

    path('product/list/', AdminProductListView.as_view(), name="adminproductlist"),
    path("product/add/", AdminProductCreateView.as_view(), name="adminproductcreate"),
    
    path('home/', AdminHomeView.as_view(), name='adminhome'),
    path('order/<int:pk>', AdminOrderDetailView.as_view(), name='adminorderdetail'),
    path('all-orders/', AdminOrderListView.as_view(), name='adminorderlist'),
    path('product/update/<int:pk>', AdminProductUpdateView.as_view(), name='adminproductupdate'),
    path('product/delete/<int:pk>', AdminProductDeleteView.as_view(), name='adminproductdelete'),

    path('admin-order-<int:pk>-change/', AdminOrderStatusChangeView.as_view(), name="adminorderchange"),

]
