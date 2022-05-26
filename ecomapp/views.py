from django.shortcuts import redirect
from django.views.generic import View, TemplateView, CreateView
from django.urls import reverse_lazy
from .forms import CheckoutForm
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator


#assign customer to cart object
class EcomMixin(object): 
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and Customer.objects.filter(user=request.user):
                cart_obj.customer = request.user.customer
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)
    


class HomeView(EcomMixin, TemplateView):
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_list = Product.objects.all().order_by("-id")
        paginator = Paginator(product_list, 8)
        page_number = self.request.GET.get('page')
        all_products = paginator.get_page(page_number)
        context['all_products'] = all_products
        return context



class CategoryView(EcomMixin, TemplateView):
    template_name = "categories.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_categories'] = Category.objects.all()
        return context

class ProductDetailView(EcomMixin, TemplateView):
    template_name = "productdetail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        product.view_count += 1
        product.save()
        context['product'] = product
        return context

class AddToCartView(EcomMixin,TemplateView):
    template_name = "addtocart.html"
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        #get product id from requested url
        product_id = self.kwargs['pro_id']
        #get product
        product_obj = Product.objects.get(id=product_id)
        # check if cart exists
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(product=product_obj)
            
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1 
                cartproduct.subtotal += product_obj.selling_price
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
            else:
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, price=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
                cart_obj.total += product_obj.selling_price
                cart_obj.save()

            
        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            print('new cart')
            cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, price=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
            cart_obj.total += product_obj.selling_price
            cart_obj.save()

        return context

class CartView(EcomMixin, TemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context


class ManageCartView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        print("this is manage cart section.")
        cproduct_id = self.kwargs["cproduct_id"]
        action = request.GET.get("action")
        cproduct_obj = CartProduct.objects.get(id=cproduct_id)
        cart_obj = cproduct_obj.cart

        
        if action == "inc":
            cproduct_obj.quantity += 1
            cproduct_obj.subtotal += cproduct_obj.price
            cproduct_obj.save()
            cart_obj.total += cproduct_obj.price
            cart_obj.save()
        elif action == "dcr":
            cproduct_obj.quantity -= 1
            cproduct_obj.subtotal -= cproduct_obj.price
            cproduct_obj.save()
            cart_obj.total -= cproduct_obj.price
            cart_obj.save()
            if cproduct_obj.quantity == 0:
                cproduct_obj.delete()
        elif action == "rmv":
            cart_obj.total -= cproduct_obj.subtotal
            cart_obj.save()
            cproduct_obj.delete()
        else:
            pass
        return redirect("ecomapp:cart")

class EmptyCartView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect("ecomapp:cart")


class CheckoutView(EcomMixin, CreateView):
    template_name = "checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy('ecomapp:home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user):
            pass
        else:
            return redirect("/customer/login?next=/checkout/")
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get('cart_id')
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = 'Order Recieved'
            del self.request.session['cart_id']

        else:
            return redirect('ecomapp:home')
        return super().form_valid(form)

class SearchView(TemplateView):
    template_name= 'search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keyword = self.request.GET['keyword']
        results = Product.objects.filter(Q(title__contains=keyword) | Q(description__contains=keyword) | Q(return_policy__contains=keyword) | Q(author__contains=keyword))
        context['results'] = results
        return context

class AboutView(EcomMixin, TemplateView):
    template_name = "about.html"

class ContactView(EcomMixin, TemplateView):
    template_name = "contact.html"