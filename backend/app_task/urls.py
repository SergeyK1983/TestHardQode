from django.urls import path

from .views import ProductsListAPIView, ProductLessonsListAPIView

urlpatterns = [
    path('v1/products-list/', ProductsListAPIView.as_view(), name='products-list'),
    path('v1/product/<int:pk>/lessons/', ProductLessonsListAPIView.as_view(), name='product-lessons'),
]

