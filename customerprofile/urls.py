from django.urls import path
from .views import *

app_name = "customerprofile"

urlpatterns = [
    path("", CustomerProfileView.as_view(), name="customerprofile"),
    path("order-<int:pk>/", CustomerOrderDetailView.as_view(), name="customerorderdetail"),
    path("register/", CustomerRegistrationView.as_view(), name="customerregistration"),
    path('logout/', CustomerLogoutView.as_view(), name='customerlogout'),
    path('login/', CustomerLoginView.as_view(), name='customerlogin'),

    path('forgot-password/', PasswordForgotView.as_view(), name="passwordforgot"),
    path('password-reset/<email>/<token>/', PasswordResetView.as_view(), name='passwordreset'),

]
