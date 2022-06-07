import django_filters
from django_filters import DateFilter

from .models import *

class  order_filter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date",lookup_expr='gte')
    end_date = DateFilter(field_name="date",lookup_expr='lte')
    class Meta:
        model = Expenses
        fields = '__all__'
        exclude = ['user_custom','amount_expenses','description']

class  order_filter_earnings(django_filters.FilterSet):
    start_date = DateFilter(field_name="date",lookup_expr='gte')
    end_date = DateFilter(field_name="date",lookup_expr='lte')
    class Meta:
        model = Earnings
        fields = '__all__'
        exclude = ['user_custom','amount_earnings','description']
