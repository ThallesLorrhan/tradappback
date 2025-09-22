from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChapelViewSet

router = DefaultRouter()
router.register(r'chapels', ChapelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
