# ruff: noqa: I001
from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from records.models import Record
from users.models import User


class Command(BaseCommand):
    help = "Populate the database with 3 users and 200 sample records for API testing."

    PASSWORD = "SeedPass@123"  # noqa: S105
    RECORD_COUNT = 200

    @transaction.atomic
    def handle(self, *args, **options):
        users = self._create_users()
        Record.objects.filter(created_by__in=users).delete()
        created_records = self._create_records(users)

        self.stdout.write(self.style.SUCCESS("Database populated successfully."))
        self.stdout.write("Created users: analyst, viewer, admin")
        self.stdout.write(f"Created records: {created_records}")
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

    def _create_records(self, users):
        today = timezone.localdate()
        record_templates = [
            {
                "type": Record.Type.INCOME,
                "category": Record.Category.SALARY,
                "amount": Decimal("5000.00"),
                "description": "Monthly salary",
            },
            {
                "type": Record.Type.EXPENSE,
                "category": Record.Category.FOOD,
                "amount": Decimal("45.50"),
                "description": "Lunch expense",
            },
            {
                "type": Record.Type.EXPENSE,
                "category": Record.Category.TRANSPORT,
                "amount": Decimal("18.25"),
                "description": "Travel to office",
            },
            {
                "type": Record.Type.INCOME,
                "category": Record.Category.BONUS,
                "amount": Decimal("250.00"),
                "description": "Performance bonus",
            },
        ]

        records_to_create = []
        for index in range(self.RECORD_COUNT):
            user = users[index % len(users)]
            template = record_templates[index % len(record_templates)]
            records_to_create.append(
                Record(
                    created_by=user,
                    type=template["type"],
                    category=template["category"],
                    amount=template["amount"] + Decimal(index % 20),
                    date=today - timedelta(days=index % 30),
                    description=f'{template["description"]} #{index + 1}',
                )
            )

        Record.objects.bulk_create(records_to_create, batch_size=200)
        return len(records_to_create)
