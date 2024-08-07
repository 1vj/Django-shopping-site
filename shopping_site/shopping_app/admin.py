from django.contrib import admin
from .models import User, cart,item,wishlist

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display =['id','name','email','username','password','is_admin','cart_item','cart_value','order_value','is_authenticated']


@admin.register(item)
class itemAdmin(admin.ModelAdmin):
    list_display =['id','item_name','desc','discounted_price','available_number','image']

@admin.register(cart)
class cartAdmin(admin.ModelAdmin):
    list_display = ['user']

@admin.register(wishlist)
class wishlistAdmin(admin.ModelAdmin):
    list_display = ['user']