from genericpath import exists
from django import views
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView, CreateView, FormView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from ecomapp.forms import CheckoutForm, CustomerRegistrationForm, CustomerLoginForm
from ecomapp.models import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin



class CustomerProfileView(TemplateView):
    template_name = 'customerprofile.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/login?next=/checkout/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        context['customer'] = customer
        orders = Order.objects.filter(cart__customer=customer).order_by('-id')
        context['orders'] = orders
        return context


class CustomerOrderDetailView(DetailView):
    template_name = 'customerorderdetail.html'
    model = Order
    context_object_name = 'order_obj'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            order_id = self.kwargs["pk"]
            order = Order.objects.get(id=order_id)
            if request.user.customer != order.cart.customer:
                return redirect("customerprofile:customerprofile")
        else:
            return redirect("/login?next=/checkout/")
        return super().dispatch(request, *args, **kwargs)

        # TO DO CREATE UPDATE PROFILE AND UPDATE USER 

