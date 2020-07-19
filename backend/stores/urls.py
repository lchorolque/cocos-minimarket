from django.urls import include, path
from rest_framework import routers
from backend.stores.views import StoreViewSet, StoreStockViewSet


router = routers.DefaultRouter()
router.register('stocks', StoreStockViewSet, basename='store-stocks')
router.register('', StoreViewSet, basename='stores')

urlpatterns = [
    path('', include(router.urls)),
]
