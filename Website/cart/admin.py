from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user','product')
