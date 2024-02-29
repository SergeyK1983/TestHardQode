from rest_framework import generics, permissions

from .models import Product
from .serializer import ProductSerializer, ProductLessonsSerializer


class ProductsListAPIView(generics.ListAPIView):
    """
    Контроллер списка продуктов, доступных для покупки, который включает в себя основную информацию о
    продукте и количество уроков, принадлежащих продукту.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductLessonsListAPIView(generics.ListAPIView):
    """
    Контроллер вывода списка уроков по конкретному продукту к которому пользователь имеет доступ.
    Условно считаем, что пользователь аутентифицирован и авторизован, переходит по ссылке.
    """
    serializer_class = ProductLessonsSerializer

    def get_queryset(self):
        return Product.objects.filter(id=self.kwargs['pk'])

