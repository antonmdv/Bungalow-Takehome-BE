from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import HouseViewSet

router = DefaultRouter()
router.register(r'houses', HouseViewSet, basename='house')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]
