from django.urls import path
from . import views

app_name = 'order'
urlpatterns=[
    path('<int:order_id>/',views.order_details,name='order_details'),
    path('create_order/',views.create_order,name='create_order'),
    path('coupon/<int:order_id>/',views.coupon_order,name='coupon'),
    path('request/<int:order_id>/<int:price>/', views.send_request, name='request'),
    path('verify/', views.verify , name='verify'),
]