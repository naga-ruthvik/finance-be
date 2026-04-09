from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import TransactionView

router = DefaultRouter()
router.register(r"", TransactionView, basename="transactions")

urlpatterns = router.urls
