from decimal import Decimal

from rest_framework import serializers

from .models import Record


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = [
            "id",
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
            "id": {"read_only": True},
        }

    def validate(self, data):
        """
        Validate that the chosen category matches the record type.
        """
        # Handle partial updates by getting existing values if not provided in data
        record_type = data.get("type")
        category = data.get("category")

        if self.instance:
            if record_type is None:
                record_type = self.instance.type
            if category is None:
                category = self.instance.category

        # Define category groupings based on the Record model
        income_categories = {
            Record.Category.SALARY,
            Record.Category.FREELANCE,
            Record.Category.BUSINESS,
            Record.Category.INVESTMENT,
            Record.Category.BONUS,
            Record.Category.OTHER_INCOME,
        }

        expense_categories = {
            Record.Category.FOOD,
            Record.Category.RENT,
            Record.Category.TRANSPORT,
            Record.Category.UTILITIES,
            Record.Category.ENTERTAINMENT,
            Record.Category.HEALTH,
            Record.Category.SHOPPING,
            Record.Category.EDUCATION,
            Record.Category.TRAVEL,
        }

        # Perform the validation
        if record_type == Record.Type.INCOME and category not in income_categories:
            raise serializers.ValidationError(
                {"category": f"'{category}' is not a valid category for income."}
            )

        if record_type == Record.Type.EXPENSE and category not in expense_categories:
            raise serializers.ValidationError(
                {"category": f"'{category}' is not a valid category for expense."}
            )

        return data


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
