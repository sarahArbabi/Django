from django.db import models
from home.models import Product,Variant
from django.contrib.auth.models import User
from django.forms import ModelForm
# Create your models here.
class Cart(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant,on_delete=models.CASCADE,blank=True,null=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.user.username


class CartForm(ModelForm):
    class Meta:
        model = Cart
        fields =('quantity',)
