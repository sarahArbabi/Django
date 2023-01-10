from django.urls import path
from . import views

app_name = 'home'

urlpatterns=[
    path('',views.home,name='home'),
    path('products/',views.all_products,name='products'),
    path('details/<int:id>/',views.details,name='details'),
    path('category/<int:id>/<slug:slug>/',views.all_products,name='category'),
    path('like/<int:id>/',views.product_like,name='like'),
    path('dislike/<int:id>/',views.product_dislike,name='dislike'),
    path('comment/<int:id>/',views.product_comment,name='comment'),
    path('reply/<int:id>/<int:comment_id>/',views.product_reply,name='reply'),
    path('search/',views.product_search,name='search'),
    path('favorite/<int:id>/',views.favorite,name='favorite'),
    path('contact/',views.contact,name='contact'),
    path('compare/<int:id>/',views.compare,name='compare'),
    path('show/',views.show,name='show'),
    path('view/',views.product_view,name='product_view'),
]