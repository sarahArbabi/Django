from django.db import models
from django.contrib.auth.models import User
from home.models import *
from django.forms import ModelForm
# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    create = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    discount = models.PositiveIntegerField(blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.TextField()

    def __str__(self):
        return self.user.username

    def get_price(self):
        total = sum(i.price() for i in self.order_item.all())
        if self.discount:
            discount_price =(self.discount * total) / 100
            return int(total-discount_price)
        return total


class ItemOrder(models.Model):
    order= models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_item')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.user.username

    def price(self):
        if self.product.status != 'None':
            return self.variant.total_price * self.quantity
        else:
            return self.product.total_price * self.quantity


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields=('email','first_name','last_name','address')




class Coupon(models.Model):
    code= models.CharField(max_length=100,unique=True)
    active = models.BooleanField(default=False)
    start = models.DateTimeField()
    end = models.DateTimeField()
    discount = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return self.code