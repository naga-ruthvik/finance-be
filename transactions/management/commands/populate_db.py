# ruff: noqa: I001
from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from transactions.models import Transaction
from users.models import User


class Command(BaseCommand):
    help = "Populate the database with 3 users and 200 sample transactions for API testing."

    PASSWORD = "SeedPass@123"  # noqa: S105
    Transaction_COUNT = 200

    @transaction.atomic
    def handle(self, *args, **options):
        users = self._create_users()
        Transaction.objects.filter(created_by__in=users).delete()
        created_transactions = self._create_transactions(users)

        self.stdout.write(self.style.SUCCESS("Database populated successfully."))
        self.stdout.write("Created users: analyst, viewer, admin")
        self.stdout.write(f"Created transactions: {created_transactions}")
        self.stdout.write(f"All seeded users use password: {self.PASSWORD}")

    def _create_users(self):
        user_specs = [
            {
                "username": "analyst",
                "role": User.Role.ANALYST,
                "first_name": "Analyst",
                "last_name": "User",
                "is_staff": False,
                "is_superuser": False,
            },
            {
                "username": "viewer",
                "role": User.Role.VIEWER,
                "first_name": "Viewer",
                "last_name": "User",
                "is_staff": False,
                "is_superuser": False,
            },
            {
                "username": "admin",
                "role": User.Role.ADMIN,
                "first_name": "Admin",
                "last_name": "User",
                "is_staff": True,
                "is_superuser": True,
            },
        ]

        users = []
        for spec in user_specs:
            user, _ = User.objects.update_or_create(
                username=spec["username"],
                defaults={
                    "email": f"{spec['username']}@example.com",
                    "first_name": spec["first_name"],
                    "last_name": spec["last_name"],
                    "role": spec["role"],
                    "is_staff": spec["is_staff"],
                    "is_superuser": spec["is_superuser"],
                    "is_active": True,
                },
            )
            user.set_password(self.PASSWORD)
            user.save(update_fields=["password"])
            users.append(user)

        return users

    def _create_transactions(self, users):
        today = timezone.localdate()
        Transaction_templates = [
            {
                "type": Transaction.Type.INCOME,
                "category": Transaction.Category.SALARY,
                "amount": Decimal("5000.00"),
                "description": "Monthly salary",
            },
            {
                "type": Transaction.Type.EXPENSE,
                "category": Transaction.Category.FOOD,
                "amount": Decimal("45.50"),
                "description": "Lunch expense",
            },
            {
                "type": Transaction.Type.EXPENSE,
                "category": Transaction.Category.TRANSPORT,
                "amount": Decimal("18.25"),
                "description": "Travel to office",
            },
            {
                "type": Transaction.Type.INCOME,
                "category": Transaction.Category.BONUS,
                "amount": Decimal("250.00"),
                "description": "Performance bonus",
            },
        ]

        transactions_to_create = []
        for index in range(self.Transaction_COUNT):
            user = users[index % len(users)]
            template = Transaction_templates[index % len(Transaction_templates)]
            transactions_to_create.append(
                Transaction(
                    created_by=user,
                    type=template["type"],
                    category=template["category"],
                    amount=template["amount"] + Decimal(index % 20),
                    date=today - timedelta(days=index % 30),
                    description=f'{template["description"]} #{index + 1}',
                )
            )

        Transaction.objects.bulk_create(transactions_to_create, batch_size=200)
        return len(transactions_to_create)
