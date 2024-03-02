from django.urls import path

from .views import ProductsListAPIView, ProductLessonsListAPIView, ProductStudentsListAPIView, GroupFullnessListAPIView, \
    ProductsPercentageListAPIView

urlpatterns = [
    path('v1/products-list/', ProductsListAPIView.as_view(), name='products-list'),
    path('v1/product-percentage/', ProductsPercentageListAPIView.as_view(), name='product-percentage'),
    path('v1/product/<int:pk>/lessons/', ProductLessonsListAPIView.as_view(), name='product-lessons'),
    path('v1/product/<int:pk>/students/', ProductStudentsListAPIView.as_view(), name='product-students'),
    path('v1/groups-fullness/', GroupFullnessListAPIView.as_view(), name='groups-fullness'),
]

