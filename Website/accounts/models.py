from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.IntegerField(blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    profile_image = models.ImageField(upload_to='profile/',blank=True,null=True,default='images.png')

    def __str__(self):
        return self.user.username


def save_profile_user(sender,**kwargs):
    if kwargs['created']:
        profile_user = Profile(user=kwargs['instance'])
        profile_user.save()


post_save.connect(save_profile_user,sender = User)
