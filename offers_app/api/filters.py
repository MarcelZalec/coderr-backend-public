from django_filters import FilterSet, NumberFilter
from offers_app.models import Offer
from django.db.models import Min


class OfferFilter(FilterSet):
    """
    FilterSet for filtering Offer instances based on various criteria.

    Attributes:
    - creator_id (NumberFilter): Filters offers by creator (user).
    - min_price (NumberFilter): Filters offers based on the minimum price.
    - max_delivery_time (NumberFilter): Filters offers by maximum delivery time.

    Meta:
    - model: Offer model.
    - fields: ['creator_id', 'min_price', 'max_delivery_time'].

    Methods:
    - filter_min_price(queryset, name, value): Filters queryset by minimum price.
    - filter_max_delivery_time(queryset, name, value): Filters queryset by maximum delivery time.
    """
    creator_id = NumberFilter(field_name='user')
    min_price = NumberFilter(method='filter_min_price')
    max_delivery_time = NumberFilter(method='filter_max_delivery_time')

    class Meta:
        model = Offer
        fields = ['creator_id', 'min_price', 'max_delivery_time']

    def filter_min_price(self, queryset, name, value):
        return queryset.annotate(min_price=Min('details__price')).filter(min_price__gte=value)

    def filter_max_delivery_time(self, queryset, name, value):
        return queryset.annotate(min_delivery_time=Min('details__delivery_time_in_days')).filter(min_delivery_time__lte=value)