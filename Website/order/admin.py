from django.contrib import admin
from .models import *
# Register your models here.

class ItemInlines(admin.TabularInline):
    model = ItemOrder
    readonly_fields = ('user','product','quantity','price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','email','first_name','last_name','create','paid','get_price')
    inlines = [ItemInlines]

class CouponAdmin(admin.ModelAdmin):
    list_display = ('code','start','end','discount')



admin.site.register(ItemOrder)
admin.site.register(Coupon,CouponAdmin)