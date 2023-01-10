from django.contrib import admin
from .models import *
import admin_thumbnails
# Register your models here.
class ProductVariantInlines(admin.TabularInline):
    model = Variant
    extra = 2


@admin_thumbnails.thumbnail('image')
class ImageInlines(admin.TabularInline):
    model = Images
    extra = 3



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'sub_cat','create','update')
    prepopulated_fields = {'slug':('name',)}




@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','available','amount','create','update','unit_price','discount','total_price','num_view')
    inlines = [ProductVariantInlines,ImageInlines]
    list_editable = ('amount',)




@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user','comment','create')


@admin.register(Compare)
class CompareAdmin(admin.ModelAdmin):
    list_display = ('user','product','session_key')

admin.site.register(Size)
admin.site.register(Color)

admin.site.register(Variant)
admin.site.register(Images)
admin.site.register(Brand)
admin.site.register(Views)