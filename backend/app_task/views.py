from django.shortcuts import render
from rest_framework import generics, permissions, status

from .models import Product
from .serializer import ProductSerializer


class ProductsListAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

