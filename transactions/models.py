from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import TextChoices

# Create your models here.


class Transaction(models.Model):

    class Type(TextChoices):
        INCOME = "INCOME", "income"
        EXPENSE = "EXPENSE", "expense "

    class Category(models.TextChoices):
        # Expense categories
        FOOD = "FOOD", "Food"
        RENT = "RENT", "Rent"
        TRANSPORT = "TRANSPORT", "Transport"
        UTILITIES = "UTILITIES", "Utilities"  # electricity, water, etc.
        ENTERTAINMENT = "ENTERTAINMENT", "Entertainment"
        HEALTH = "HEALTH", "Health"
        SHOPPING = "SHOPPING", "Shopping"
        EDUCATION = "EDUCATION", "Education"
        TRAVEL = "TRAVEL", "Travel"

        # Income categories
        SALARY = "SALARY", "Salary"
        FREELANCE = "FREELANCE", "Freelance"
        BUSINESS = "BUSINESS", "Business"
        INVESTMENT = "INVESTMENT", "Investment"
        BONUS = "BONUS", "Bonus"
        OTHER_INCOME = "OTHER_INCOME", "Other Income"

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    type = models.CharField(max_length=10, choices=Type.choices)
    date = models.DateField()
    description = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=Category.choices)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.date} - {self.type} - {self.amount}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
