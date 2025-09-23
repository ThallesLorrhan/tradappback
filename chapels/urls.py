# chapels/urls.py
from rest_framework.routers import DefaultRouter
from .views import ChapelViewSet

router = DefaultRouter()
router.register(r'chapels', ChapelViewSet)

urlpatterns = router.urls
