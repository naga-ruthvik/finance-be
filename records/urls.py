from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import RecordView

router = DefaultRouter()
router.register(r"", RecordView, basename="records")

urlpatterns = router.urls
