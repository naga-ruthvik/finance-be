from django.db import models
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.utils.timezone import now

from ..models import Transaction


# 🔹 Base queryset
def get_base_queryset():
    return Transaction.objects.all()


# 🔹 Total income, expense, transactions (1 query)
def get_income_expense_totals():
    data = get_base_queryset().aggregate(
        total_income=Sum("amount", filter=models.Q(type=Transaction.Type.INCOME)),
        total_expense=Sum("amount", filter=models.Q(type=Transaction.Type.EXPENSE)),
        total_transactions=Count("id"),
    )

    return {
        "total_income": data["total_income"] or 0,
        "total_expense": data["total_expense"] or 0,
        "total_transactions": data["total_transactions"] or 0,
    }


# 🔹 Category-wise totals
def get_category_totals(Transaction_type):
    return list(
        get_base_queryset()
        .filter(type=Transaction_type)
        .values("category")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )


# 🔹 Top expense category
def get_top_expense_category():
    return (
        get_base_queryset()
        .filter(type=Transaction.Type.EXPENSE)
        .values("category")
        .annotate(total=Sum("amount"))
        .order_by("-total")
        .first()
    )


# 🔹 Monthly trends
def get_monthly_trends():
    qs = get_base_queryset().annotate(month=TruncMonth("date"))

    data = (
        qs.values("month")
        .annotate(
            income=Sum("amount", filter=models.Q(type=Transaction.Type.INCOME)),
            expense=Sum("amount", filter=models.Q(type=Transaction.Type.EXPENSE)),
        )
        .order_by("month")
    )

    return [
        {
            "month": item["month"].strftime("%Y-%m"),  # Apr, May, etc.
            "income": item["income"] or 0,
            "expense": item["expense"] or 0,
        }
        for item in data
    ]

    return [
        {
            "month": item["month"],
            "income": item["income"] or 0,
            "expense": item["expense"] or 0,
        }
        for item in data
    ]


# 🔹 Current month summary
def get_current_month_summary():
    today = now()

    qs = get_base_queryset().filter(date__month=today.month, date__year=today.year)

    data = qs.aggregate(
        income=Sum("amount", filter=models.Q(type=Transaction.Type.INCOME)),
        expense=Sum("amount", filter=models.Q(type=Transaction.Type.EXPENSE)),
    )

    return {
        "income": data["income"] or 0,
        "expense": data["expense"] or 0,
    }


# 🔹 Recent activity
def get_recent_activity(limit=5):
    return list(
        get_base_queryset()
        .order_by("-created_at")
        .values("id", "type", "amount", "category", "date")[:limit]
    )


# 🔥 MAIN FUNCTION
def get_dashboard_summary():
    totals = get_income_expense_totals()

    total_income = totals["total_income"]
    total_expense = totals["total_expense"]

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": total_income - total_expense,
        "total_transactions": totals["total_transactions"],
        "income_by_category": get_category_totals(Transaction.Type.INCOME),
        "expense_by_category": get_category_totals(Transaction.Type.EXPENSE),
        "top_expense_category": get_top_expense_category(),
        "monthly_summary": get_current_month_summary(),
        "monthly_trends": get_monthly_trends(),
        "recent_activity": get_recent_activity(),
    }
