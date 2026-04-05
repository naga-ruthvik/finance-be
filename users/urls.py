from rest_framework.routers import DefaultRouter

from .views import UserViews

router = DefaultRouter()
router.register(r"", UserViews, basename="users")

urlpatterns = router.urls
