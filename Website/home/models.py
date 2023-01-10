from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db.models import Avg
# Create your models here.
class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE,blank=True,null=True,related_name='sub')
    sub_cat = models.BooleanField(default=False)
    name = models.CharField(max_length=50)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='category/')
    slug = models.SlugField(blank=True,null=True,allow_unicode=True,unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
         return reverse('home:category', args=[self.id,self.slug])




class Product(models.Model):
    VARIANT=(
        ('None','none'),
        ('Color','color'),
        ('Size','size'),
        ('both','Both'),
    )
    category = models.ManyToManyField(Category,blank=True)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='product/')
    amount = models.PositiveIntegerField()
    information = models.TextField(blank=True,null=True)
    available = models.BooleanField(default=True)
    unit_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(blank=True,null=True)
    total_price = models.PositiveIntegerField(blank=True,null=True)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=VARIANT,blank=True,null=True,max_length=10)
    tags = TaggableManager(blank=True)
    like = models.ManyToManyField(User,blank=True,related_name='product_like')
    total_like = models.PositiveIntegerField(default=0)
    dislike = models.ManyToManyField(User,blank=True,related_name='product_dislike')
    total_dislike = models.PositiveIntegerField(default=0)
    favorite = models.ManyToManyField(User,blank=True,related_name='fa_user')
    brand = models.ForeignKey('brand',on_delete=models.CASCADE,null=True,blank=True)
    view = models.ManyToManyField(User,blank=True,related_name='product_view')
    num_view = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.name

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.discount * self.unit_price)/100
            return int(self.unit_price - total)
        return self.total_price


    def total_like(self):
        return self.like.count()

    def total_dislike(self):
        return self.dislike.count()

    def get_absolute_url(self):
        return reverse('home:details',args=[self.id])


    def average(self):
        data = Comment.objects.filter(is_reply=False,product=self).aggregate(avg=Avg('rate',))
        star = 0
        if data['avg'] is not None:
            star = round(data['avg'],1)
        return star

class Color(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name




class Size(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name





class Variant(models.Model):
    product_variant = models.ForeignKey(Product,on_delete=models.CASCADE)
    size_variant = models.ForeignKey(Size,on_delete=models.CASCADE,blank=True,null=True)
    color_variant = models.ForeignKey(Color,on_delete=models.CASCADE ,blank=True,null=True)
    name = models.CharField(max_length=50)
    unit_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(blank=True, null=True)
    total_price = models.PositiveIntegerField(blank=True, null=True)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.discount * self.unit_price) / 100
            return int(self.unit_price - total)
        return self.total_price



class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    reply = models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True,related_name='comment_reply')
    is_reply = models.BooleanField(default=False)
    comment = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
    is_rate = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True,related_name='product_rate')
    rate = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.product.name



class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('comment','rate')





class ReplyForm(ModelForm):
    class Meta:
        model = Comment
        fields =('comment',)


class Images(models.Model):
    product_image = models.ForeignKey(Product,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,blank=True)
    image = models.ImageField(upload_to='product_image/',blank=True)



class Brand(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Compare(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    session_key = models.CharField(max_length=300,blank=True,null=True)

    def __str__(self):
        return self.product.name

class CompareForm(ModelForm):
    class Meta:
        model = Compare
        fields = ('product',)


class Views(models.Model):
    ip = models.CharField(max_length=200,null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name
