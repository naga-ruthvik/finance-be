from decimal import Decimal

from rest_framework import serializers

from .models import Record


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = [
            "type",
            "date",
            "description",
            "amount",
            "category",
            "created_by",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "created_by": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "amount": {"min_value": Decimal("0.01")},
            "description": {"allow_null": True, "required": False},
        }


class DashboardSummarySerializer(serializers.Serializer):
    """Compact serializer for the dashboard summary data."""
    total_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expense = serializers.DecimalField(max_digits=12, decimal_places=2)
    net_balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_transactions = serializers.IntegerField()

    income_by_category = serializers.ListField(child=serializers.DictField())
    expense_by_category = serializers.ListField(child=serializers.DictField())
    top_expense_category = serializers.DictField(allow_null=True)
    monthly_summary = serializers.DictField()
    monthly_trends = serializers.ListField(child=serializers.DictField())
    recent_activity = serializers.ListField(child=serializers.DictField())
