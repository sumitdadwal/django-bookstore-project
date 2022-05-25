from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'category', 'marked_price', 'selling_price']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register([Admin, Cart, CartProduct, Order, Customer])