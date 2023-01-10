import django_filters
from django import forms
from .models import *

class ProductsFilter(django_filters.FilterSet):
    Choice_1={
        ('expensive','expensive'),
        ('cheap','cheap')
    }
    Choice_2={
        ('old','old'),
        ('new','new')
    }
    price_1 = django_filters.NumberFilter(field_name='unit_price',lookup_expr='gte')
    price_2 = django_filters.NumberFilter(field_name='unit_price',lookup_expr='lte')
    brand = django_filters.ModelMultipleChoiceFilter(queryset=Brand.objects.all(),widget=forms.CheckboxSelectMultiple)
    price = django_filters.ChoiceFilter(choices=Choice_1,method='price_filter')
    create = django_filters.ChoiceFilter(choices=Choice_2,method='create_filter')

    def price_filter(self,queryset,name,value):
        data = 'unit_price' if value == 'cheap' else '-unit_price'
        return queryset.order_by(data)

    def create_filter(self,queryset,name,value):
        data = 'create' if value == 'old' else '-create'
        return queryset.order_by(data)