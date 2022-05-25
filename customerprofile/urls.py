from unicodedata import name
from django.urls import path
from .views import *

app_name = "customerprofile"

urlpatterns = [
    path("", CustomerProfileView.as_view(), name="customerprofile"),
    path("order-<int:pk>/", CustomerOrderDetailView.as_view(), name="customerorderdetail"),

]
