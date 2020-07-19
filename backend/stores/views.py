from rest_framework import viewsets, status
from backend.stores.models import Store, StoreStock, Cart
from backend.stores.serializers import StoreSerializer, StoreStockSerializer, CartSerializer,\
    UpdateCartSerializer
from backend.stores.filters import StoreFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = StoreFilter

    def get_serializer_class(self):
        if self.action == 'my_cart':
            return CartSerializer
        elif self.action == 'update_cart':
            return UpdateCartSerializer
        return StoreSerializer

    @action(methods=['patch'], detail=True, url_path='update-cart')
    def update_cart(self, request, pk=None):
        #  user can be only one cart for store
        cart = Cart.objects.get_or_create(store_id=pk, owner=self.request.user)[0]
        serializer = self.get_serializer_class()(cart, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='my-cart')
    def my_cart(self, request, pk=None):
        cart = Cart.objects.get_or_create(store_id=pk, owner=self.request.user)[0]
        serializer = self.get_serializer_class()(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StoreStockViewSet(viewsets.ModelViewSet):
    queryset = StoreStock.objects.all().select_related('store')
    serializer_class = StoreStockSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('product', 'product__name', 'store')
