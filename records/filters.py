from django import forms

from django_filters import rest_framework as filters

from .models import Record


class RecordFilter(filters.FilterSet):
    date_from = filters.DateFilter(
        field_name="date",
        lookup_expr="gte",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    date_to = filters.DateFilter(
        field_name="date",
        lookup_expr="lte",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    category = filters.CharFilter(field_name="category", lookup_expr="iexact")
    amount_min = filters.NumberFilter(field_name="amount", lookup_expr="gte")
    amount_max = filters.NumberFilter(field_name="amount", lookup_expr="lte")

    class Meta:
        model = Record
        fields = ["date_from", "date_to", "category"]
