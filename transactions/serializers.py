from decimal import Decimal

from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
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
        Validate that the chosen category matches the Transaction type.
        """
        # Handle partial updates by getting existing values if not provided in data
        Transaction_type = data.get("type")
        category = data.get("category")

        if self.instance:
            if Transaction_type is None:
                Transaction_type = self.instance.type
            if category is None:
                category = self.instance.category

        # Define category groupings based on the Transaction model
        income_categories = {
            Transaction.Category.SALARY,
            Transaction.Category.FREELANCE,
            Transaction.Category.BUSINESS,
            Transaction.Category.INVESTMENT,
            Transaction.Category.BONUS,
            Transaction.Category.OTHER_INCOME,
        }

        expense_categories = {
            Transaction.Category.FOOD,
            Transaction.Category.RENT,
            Transaction.Category.TRANSPORT,
            Transaction.Category.UTILITIES,
            Transaction.Category.ENTERTAINMENT,
            Transaction.Category.HEALTH,
            Transaction.Category.SHOPPING,
            Transaction.Category.EDUCATION,
            Transaction.Category.TRAVEL,
        }

        # Perform the validation
        if Transaction_type == Transaction.Type.INCOME and category not in income_categories:
            raise serializers.ValidationError(
                {"category": f"'{category}' is not a valid category for income."}
            )

        if Transaction_type == Transaction.Type.EXPENSE and category not in expense_categories:
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
