from django.urls import path

from .views import ProductsListAPIView

urlpatterns = [
    path('v1/products-list/', ProductsListAPIView.as_view(), name='products-list'),
]

