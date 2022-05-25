from unicodedata import name
from django.urls import path
from .views import *

app_name = "ecomapp"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("categories/", CategoryView.as_view(), name="categories"),
    path("product/<slug:slug>", ProductDetailView.as_view(), name="productdetail"),
    path("add-to-cart-<int:pro_id>/", AddToCartView.as_view(), name="addtocart"),
    path("cart/", CartView.as_view(), name="cart"),
    path("manage-cart/<int:cproduct_id>", ManageCartView.as_view(), name="managecart"),
    path("empty-cart/", EmptyCartView.as_view(), name="emptycart"),

    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("register/", CustomerRegistrationView.as_view(), name="customerregistration"),
    path('logout/', CustomerLogoutView.as_view(), name='customerlogout'),
    path('login/', CustomerLoginView.as_view(), name='customerlogin'),

    path('admin-login/', AdminLoginView.as_view(), name='adminlogin'),
    path('admin-home/', AdminHomeView.as_view(), name='adminhome'),
    path('admin-order/<int:pk>', AdminOrderDetailView.as_view(), name='adminorderdetail'),
    path('admin-all-orders/', AdminOrderListView.as_view(), name='adminorderlist'),

    path('admin-order-<int:pk>-change/', AdminOrderStatusChangeView.as_view(), name="adminorderchange"),

    path('search/', SearchView.as_view(), name='search')

]
