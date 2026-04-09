# Finance Backend API

A production-ready RESTful API for personal finance management with robust role-based access control, comprehensive
analytics, and interactive documentation.

[![Django](https://img.shields.io/badge/Django-6.0-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.17-red.svg)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

---

## 🎯 Overview

This API provides a complete solution for tracking income and expenses, analyzing spending patterns through an
intelligent dashboard, and managing users with granular role-based permissions. Built with modern best practices and
production-ready from day one.

**Key Features:**

- **JWT-based authentication** with automatic token refresh
- **Role-based access control** (Admin, Analyst, Viewer)
- **Real-time dashboard** with aggregated metrics and trends
- **Advanced filtering** by date range, category, and amount
- **Interactive API documentation** (Swagger UI & ReDoc)
- **Production-ready** with Gunicorn and PostgreSQL support
- **Type-safe** with validated categories and comprehensive error handling

---

## 📋 Table of Contents

- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Environment Setup](#-environment-setup)
- [API Documentation](#-api-documentation)
    - [Authentication](#authentication)
    - [Users](#users)
    - [Transactions](#transactions)
    - [Dashboard](#dashboard)
- [Role-Based Access Control](#-role-based-access-control)
- [Advanced Features](#-advanced-features)
- [Project Architecture](#-project-architecture)
- [Design Decisions](#-design-decisions)
- [Production Deployment](#-production-deployment)

---

## 🛠 Tech Stack

| Component           | Technology                          | 
|---------------------|-------------------------------------|
| **Framework**       | Django 6.0 + DRF 3.17               |
| **Authentication**  | JWT (djangorestframework-simplejwt) |
| **Database**        | SQLite (dev) / PostgreSQL (prod)    |
| **API Docs**        | drf-spectacular                     |
| **Validation**      | Django ORM + DRF Serializers        |
| **Code Quality**    | Ruff                                |
| **Package Manager** | uv                                  |
| **WSGI Server**     | Gunicorn                            |

---

## 🚀 Quick Start

### Prerequisites

Ensure you have the following installed:

- **Python 3.12+** ([Download](https://www.python.org/downloads/))
- **uv** package manager ([Install](https://docs.astral.sh/uv/)) *or* **pip**

### Installation

```bash
# 1. Clone the repository
git clone <repository-url>
cd finance-be

# 2. Create virtual environment and install dependencies
uv init
uv sync

# Alternative: Using pip
# python -m venv .venv
# source .venv/bin/activate  # On Windows: .venv\Scripts\activate
# pip install -r requirements.txt

# 3. Run database migrations
python manage.py migrate

# 4. Seed the database with sample data (optional but recommended)
python manage.py populate_db

# 5. Start the development server
python manage.py runserver
```

🎉 **Your API is now running at** `http://127.0.0.1:8000/`

### 📚 Explore the Interactive Docs

Once the server is running:

- **Swagger UI:** [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/) — Test endpoints interactively
- **ReDoc:** [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/) — Clean, searchable documentation
- **OpenAPI Schema:** [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/) — Raw schema for code
  generation

---

## ⚙️ Environment Setup

### Sample Users (After Seeding)

The `populate_db` command creates three ready-to-use accounts:

| Username  | Password       | Role    | Permissions                                  |
|-----------|----------------|---------|----------------------------------------------|
| `admin`   | `SeedPass@123` | ADMIN   | Full access: CRUD transactions, manage users |
| `analyst` | `SeedPass@123` | ANALYST | Read-only transactions + dashboard           |
| `viewer`  | `SeedPass@123` | VIEWER  | Dashboard only                               |

**Note:** The seed command is idempotent — re-running updates existing users and refreshes sample transactions.

### Environment Variables(Optional)

Create a `.env` file for production deployments:

```env
# Database (optional - defaults to SQLite if not set)
DATABASE_URL=postgresql://user:password@host:5432/database
```

**For local development**, no `.env` file is required — sensible defaults work out of the box.

---

## 📖 API Documentation

> **Authentication Required:** All endpoints except `/api/token/` require a valid JWT in the
`Authorization: Bearer <token>` header.

### Authentication

Obtain and refresh JWT tokens for secure API access.

#### **POST** `/api/token/`

Authenticate and receive access + refresh tokens.

**Request:**

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "SeedPass@123"
  }'
```

**Response:**

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Token Lifetimes:**

- Access token: **60 minutes**
- Refresh token: **24 hours**

#### **POST** `/api/token/refresh/`

Refresh an expired access token using your refresh token.

**Request:**

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### Users

> **Admin Only** — All user management endpoints require `ADMIN` role.

| Method   | Endpoint           | Description                      |
|----------|--------------------|----------------------------------|
| `GET`    | `/api/users/`      | List all users (paginated)       |
| `POST`   | `/api/users/`      | Create a new user                |
| `GET`    | `/api/users/{id}/` | Retrieve a specific user         |
| `PUT`    | `/api/users/{id}/` | Full update (all fields)         |
| `PATCH`  | `/api/users/{id}/` | Partial update (selected fields) |
| `DELETE` | `/api/users/{id}/` | Delete a user                    |

#### Create User Example

**Request:**

```json
{
  "username": "john_doe",
  "email": "john.doe@example.com",
  "password": "SecurePass@123",
  "role": "ANALYST"
}
```

**Response:**

```json
{
  "id": 4,
  "username": "john_doe",
  "email": "john.doe@example.com",
  "role": "ANALYST",
  "date_joined": "2026-04-09T10:30:00Z"
}
```

**Security Notes:**

- Passwords are automatically hashed using Django's secure hashing algorithm
- The `password` field is write-only and never returned in responses
- Users are created via `User.objects.create_user()` for proper password handling

---

### Transactions

Track income and expenses with comprehensive CRUD operations and validation.

| Method   | Endpoint                  | Description                   | Roles          |
|----------|---------------------------|-------------------------------|----------------|
| `GET`    | `/api/transactions/`      | List transactions (paginated) | ADMIN, ANALYST |
| `POST`   | `/api/transactions/`      | Create a transaction          | ADMIN          |
| `GET`    | `/api/transactions/{id}/` | Retrieve single transaction   | ADMIN, ANALYST |
| `PUT`    | `/api/transactions/{id}/` | Full update                   | ADMIN          |
| `PATCH`  | `/api/transactions/{id}/` | Partial update                | ADMIN          |
| `DELETE` | `/api/transactions/{id}/` | Delete a transaction          | ADMIN          |

#### Transaction Types & Categories

**Transaction Types:**

- `INCOME` — Money coming in
- `EXPENSE` — Money going out

**Expense Categories:**
`FOOD` • `RENT` • `TRANSPORT` • `UTILITIES` • `ENTERTAINMENT` • `HEALTH` • `SHOPPING` • `EDUCATION` • `TRAVEL`

**Income Categories:**
`SALARY` • `FREELANCE` • `BUSINESS` • `INVESTMENT` • `BONUS` • `OTHER_INCOME`

#### Create Transaction Example

**Request:**

```json
{
  "type": "EXPENSE",
  "date": "2026-04-09",
  "amount": "42.50",
  "category": "FOOD",
  "description": "Lunch at downtown café"
}
```

**Response:**

```json
{
  "id": 201,
  "type": "EXPENSE",
  "date": "2026-04-09",
  "amount": "42.50",
  "category": "FOOD",
  "description": "Lunch at downtown café",
  "created_by": {
    "id": 1,
    "username": "admin"
  },
  "created_at": "2026-04-09T12:45:30Z"
}
```

**Validation:**

- ✅ Categories are validated against their transaction type
- ✅ You cannot create an `INCOME` transaction with `FOOD` category
- ✅ Amount must be positive (≥ 0.01)
- ✅ `created_by` is automatically set to the authenticated user

---

### Dashboard

Real-time financial analytics and insights aggregated across all transactions.

#### **GET** `/api/dashboard/summary/`

Returns comprehensive financial metrics in a single response.

**Roles:** ADMIN, ANALYST, VIEWER

**Response Structure:**

```json
{
  "total_income": "125000.00",
  "total_expense": "87500.00",
  "net_balance": "37500.00",
  "total_transactions": 200,
  "income_by_category": {
    "SALARY": "100000.00",
    "FREELANCE": "15000.00",
    "INVESTMENT": "10000.00"
  },
  "expense_by_category": {
    "RENT": "30000.00",
    "FOOD": "18000.00",
    "TRANSPORT": "12000.00",
    "UTILITIES": "8000.00",
    "ENTERTAINMENT": "7500.00",
    "HEALTH": "6000.00",
    "SHOPPING": "4000.00",
    "EDUCATION": "1500.00",
    "TRAVEL": "500.00"
  },
  "top_expense_category": {
    "category": "RENT",
    "amount": "30000.00"
  },
  "monthly_summary": {
    "month": "2026-04",
    "income": "10000.00",
    "expense": "7200.00",
    "net": "2800.00"
  },
  "monthly_trends": [
    {
      "month": "2026-01",
      "income": "10000.00",
      "expense": "7500.00",
      "net": "2500.00"
    },
    {
      "month": "2026-02",
      "income": "12000.00",
      "expense": "8000.00",
      "net": "4000.00"
    }
  ],
  "recent_activity": [
    {
      "id": 200,
      "type": "EXPENSE",
      "category": "FOOD",
      "amount": "42.50",
      "date": "2026-04-09",
      "description": "Lunch at downtown café"
    }
  ]
}
```

**Metrics Explained:**

| Field                  | Description                                             |
|------------------------|---------------------------------------------------------|
| `total_income`         | Sum of all income transactions                          |
| `total_expense`        | Sum of all expense transactions                         |
| `net_balance`          | Difference: `total_income - total_expense`              |
| `total_transactions`   | Count of all recorded transactions                      |
| `income_by_category`   | Income totals grouped by category                       |
| `expense_by_category`  | Expense totals grouped by category                      |
| `top_expense_category` | Category with the highest total spending                |
| `monthly_summary`      | Income/expense breakdown for the current month          |
| `monthly_trends`       | Historical month-by-month income vs. expense comparison |
| `recent_activity`      | The 5 most recently created transactions                |

**Note:** Dashboard aggregates data across all users (system-wide view).

---

## 🔐 Role-Based Access Control

The API implements a three-tier permission model for fine-grained access control.

| Role        | Transactions (Read) | Transactions (Write) | User Management | Dashboard |
|-------------|:-------------------:|:--------------------:|:---------------:|:---------:|
| **ADMIN**   |          ✅          |          ✅           |        ✅        |     ✅     |
| **ANALYST** |          ✅          |          ❌           |        ❌        |     ✅     |
| **VIEWER**  |          ❌          |          ❌           |        ❌        |     ✅     |

### Role Details

**🔴 ADMIN**

- Full system access
- Create, read, update, and delete all transactions
- Manage user accounts and roles
- Access all dashboard metrics

**🟡 ANALYST**

- Read-only access to transaction data
- View dashboard analytics
- Perfect for financial reporting and analysis
- Cannot modify data or manage users

**🟢 VIEWER**

- Dashboard access only
- Ideal for stakeholders who need high-level insights
- Cannot access raw transaction data
- No modification permissions

### Implementation

Permissions are enforced via custom DRF permission classes:

- `IsAdmin` — Allows only ADMIN role
- `IsAnalyst` — Allows ADMIN and ANALYST roles
- `CanViewTransactions` — Allows ADMIN and ANALYST for transaction reads
- View-level permission checks ensure unauthorized access is blocked before reaching business logic

---

## 🔍 Advanced Features

### Filtering

Apply powerful filters to the `/api/transactions/` endpoint:

| Parameter    | Type    | Example                 | Description                         |
|--------------|---------|-------------------------|-------------------------------------|
| `category`   | string  | `?category=food`        | Case-insensitive category filter    |
| `date_from`  | date    | `?date_from=2026-01-01` | Transactions on or after this date  |
| `date_to`    | date    | `?date_to=2026-03-31`   | Transactions on or before this date |
| `amount_min` | decimal | `?amount_min=100`       | Minimum amount (inclusive)          |
| `amount_max` | decimal | `?amount_max=500`       | Maximum amount (inclusive)          |

**Combine multiple filters:**

```
GET /api/transactions/?category=food&date_from=2026-01-01&amount_max=100
```

This returns all food expenses between January 1, 2026 and today, under $100.

### Ordering

Sort results by `amount` or `date`:

```bash
# Ascending by amount
GET /api/transactions/?ordering=amount

# Descending by date (most recent first)
GET /api/transactions/?ordering=-date

# Combine with filters
GET /api/transactions/?category=rent&ordering=-amount
```

**Default:** Transactions are ordered by `-created_at` (newest first).

### Pagination

All list endpoints use page-number pagination:

| Parameter   | Default | Maximum | Description                |
|-------------|---------|---------|----------------------------|
| `page`      | 1       | —       | Page number to retrieve    |
| `page_size` | 10      | 100     | Number of results per page |

**Example Request:**

```
GET /api/transactions/?page=2&page_size=25
```

**Paginated Response:**

```json
{
  "count": 200,
  "next": "http://127.0.0.1:8000/api/transactions/?page=3&page_size=25",
  "previous": "http://127.0.0.1:8000/api/transactions/?page=1&page_size=25",
  "results": [
    {
      "id": 26,
      "type": "EXPENSE",
      ...
    },
    {
      "id": 27,
      "type": "INCOME",
      ...
    }
  ]
}
```

---

## 🏗 Project Architecture

### Directory Structure

```
finance-be/
├── finance/                       # Django project settings
│   ├── settings.py                # Configuration (DB, auth, REST framework)
│   ├── urls.py                    # Root URL routing
│   ├── wsgi.py                    # WSGI entry point (Gunicorn)
│   └── asgi.py                    # ASGI entry point
│
├── users/                         # User management app
│   ├── models.py                  # Custom User model with role field
│   ├── serializers.py             # User serializer (write-only password)
│   ├── views.py                   # UserViewSet (admin-only CRUD)
│   ├── permissions.py             # Custom permission classes
│   └── urls.py                    # Router registration
│
├── transactions/                  # Core financial data app
│   ├── models.py                  # Transaction model
│   ├── serializers.py             # Transaction serializer with validation
│   ├── views.py                   # TransactionViewSet + DashboardView
│   ├── filters.py                 # TransactionFilter (date, category, amount)
│   ├── pagination.py              # Custom pagination settings
│   ├── services/
│   │   └── dashboard.py           # Business logic for aggregations
│   └── management/
│       └── commands/
│           └── populate_db.py     # Database seeding command
│
├── static/                        # Static files (collected for production)
├── schema.yml                     # Auto-generated OpenAPI 3.0 spec
├── pyproject.toml                 # Project metadata and dependencies
├── ruff.toml                      # Linter/formatter configuration
├── requirements.txt               # Pinned dependencies
├── .env.example                   # Environment variable template
└── manage.py                      # Django CLI
```

### Design Patterns

**Service Layer Pattern**

- Dashboard aggregation logic lives in `transactions/services/dashboard.py`
- Keeps views thin and business logic testable
- Each function performs a focused ORM query
- Main `get_dashboard_summary()` composes individual aggregations

**ViewSets & Routers**

- Uses DRF's `ModelViewSet` for standard CRUD operations
- Automatic URL routing via `DefaultRouter`
- Consistent API patterns across all resources

**Custom Permissions**

- Role-based permissions implemented as reusable DRF permission classes
- Enforced at the view level before any business logic executes
- Clear separation between authentication and authorization

---

## 💡 Design Decisions

### Key Assumptions

1. **System-Wide Dashboard**
    - Dashboard aggregates across all transactions (not per-user)
    - Reflects typical use case: shared finance tracking for a team/company

2. **Hardcoded Categories**
    - Transaction categories defined as model `TextChoices`
    - Avoids extra database table and joins
    - Type-safe in Python with IDE autocomplete
    - Trade-off: Adding categories requires code change + migration

3. **Positive Amounts Only**
    - All amounts must be ≥ 0.01
    - Transaction type (`INCOME`/`EXPENSE`) determines the financial direction
    - Prevents confusion with negative values

4. **No Self-Service Registration**
    - Users created by admins only (via API or seed command)
    - Appropriate for internal/corporate tools
    - Self-service signup could be added if needed

5. **JWT Over Sessions**
    - Stateless authentication scales horizontally
    - Frontend-friendly (mobile apps, SPAs)
    - No server-side session storage required

### Architectural Trade-offs

| Decision                 | ✅ Benefits                                         | ⚠️ Considerations                                    |
|--------------------------|----------------------------------------------------|------------------------------------------------------|
| **SQLite as default DB** | Zero-config local setup, no Docker required        | Not production-suitable (use `DATABASE_URL` env var) |
| **Hardcoded categories** | Type-safe, no migrations for lookups, fast queries | Adding categories requires code change               |

---

## 🚀 Production Deployment

**API URL:** `https://finance-be-84st.onrender.com/`

**Swagger Docs:** `https://finance-be-84st.onrender.com/api/docs/`

### Environment Configuration

The project is configured for deployment on Render using Gunicorn. Ensure `DATABASE_URL` is set in your environment
variables to switch from SQLite to PostgreSQL.

### Environment Configuration

**Required Environment Variables:**

```bash
DATABASE_URL=postgresql://user:password@host:5432/database
```

## 📝 Code Quality

The project uses **Ruff** for linting and formatting:

```bash
# Check code quality
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .
```

Configuration in `ruff.toml` enforces Django best practices and Python 3.12+ idioms.

---


