from django.http import Http404
from django.shortcuts import render

from django.shortcuts import redirect, render
from django.views.generic import View, TemplateView, CreateView, FormView, DetailView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from ecomapp.forms import  CustomerLoginForm, ProductForm
from .models import *
from ecomapp.models import ProductImage, Product, Order, ORDER_STATUS


class AdminLoginView(FormView):
    template_name = 'adminpages/adminlogin.html'
    form_class = CustomerLoginForm
    success_url = reverse_lazy('ecomadmin:adminhome')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        usr = authenticate(username=username, password=password)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {'form': self.form_class, 'error': 'Invalid credentials'})
        return super().form_valid(form)


class AdminRequredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/bookstore-admin/login/")
        return super().dispatch(request, *args, **kwargs)


class AdminHomeView(AdminRequredMixin, TemplateView):
    template_name = 'adminpages/adminhome.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/bookstore-admin/login")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pendingorders'] = Order.objects.filter(order_status="Order Recieved").order_by('-id')
        return context



class AdminOrderDetailView(AdminRequredMixin, DetailView):
    template_name = 'adminpages/adminorderdetail.html'
    model = Order
    context_object_name = 'order_obj'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['allstatus'] = ORDER_STATUS
        return context

class AdminOrderListView(AdminRequredMixin, ListView):
    template_name = 'adminpages/adminorderlist.html'
    queryset = Order.objects.all().order_by('-id')
    context_object_name = 'allorders'

class  AdminOrderStatusChangeView(AdminRequredMixin ,View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs["pk"]
        order_obj = Order.objects.get(id=order_id)
        new_status = request.POST.get('status')
        order_obj.order_status = new_status
        order_obj.save()
        return redirect(reverse_lazy("ecomadmin:adminorderdetail", kwargs={'pk': order_id}))

class AdminProductListView(AdminRequredMixin, ListView):
    template_name = 'adminpages/adminproductlist.html' 
    queryset = Product.objects.all().order_by("-id")
    context_object_name = "allproducts"

class AdminProductCreateView(AdminRequredMixin, CreateView):
    template_name = "adminpages/adminproductcreate.html"
    form_class = ProductForm
    success_url = reverse_lazy("ecomadmin:adminproductlist")

    def form_valid(self, form):
        prod = form.save()
        form.instance.sold_by = self.request.user.admin
        images = self.request.FILES.getlist("more_images") 
        for i in images:
            ProductImage.objects.create(product=prod, image=i)
        return super().form_valid(form)

class AdminProductUpdateView(AdminRequredMixin, UpdateView):
    template_name = "adminpages/adminproductupdate.html"
    form_class = ProductForm
    success_url=  reverse_lazy("ecomadmin:adminproductlist")
    queryset = Product.objects.all()

    def dispatch(self, request, *args, **kwargs):
        prod_obj = self.get_object()
        if prod_obj.sold_by != self.request.user.admin:
            raise Http404("Not Authorised")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        prod = form.save()
        form.instance.sold_by = self.request.user.admin
        images = self.request.FILES.getlist("more_images") 
        for i in images:
            ProductImage.objects.create(product=prod, image=i)
        return super().form_valid(form)

class AdminProductDeleteView(AdminRequredMixin, DeleteView):
    model = Product
    template_name = 'adminpages/adminproductdelete.html'
    success_url = reverse_lazy('ecomadmin:adminproductlist')