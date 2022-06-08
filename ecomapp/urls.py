from unicodedata import name
from django.urls import path
from .views import *

app_name = "ecomapp"

urlpatterns = [
    path("", home, name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("categories/", categories, name="categories"),
    path("product/<slug:slug>", ProductDetailView.as_view(), name="productdetail"),
    path("add-to-cart-<int:pro_id>/", AddToCartView.as_view(), name="addtocart"),
    path("cart/", CartView.as_view(), name="cart"),
    path("manage-cart/<int:cproduct_id>", ManageCartView.as_view(), name="managecart"),
    path("empty-cart/", EmptyCartView.as_view(), name="emptycart"),

    path("checkout/", CheckoutView.as_view(), name="checkout"),

    path('search/', SearchView.as_view(), name='search'),

    # path('create-checkout-session', CreateCheckoutSessionView.as_view(), name='createcheckoutsession')

]
