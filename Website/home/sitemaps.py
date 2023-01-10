from django.contrib.sitemaps import Sitemap
from .models import Product



class ProductViewSiteMap(Sitemap):
    changefreq = 'Never'
    priority =1

    def items(self):
        return Product.objects.all().order_by('-id')
    def lastmode(self,obj):
        return obj.create