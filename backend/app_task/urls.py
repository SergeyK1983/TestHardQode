from django.urls import path

from .views import ProductsListAPIView, ProductLessonsListAPIView, ProductStudentsListAPIView, GroupFullnessListAPIView, \
    ProductsStatisticsListAPIView

urlpatterns = [
    path('v1/products-list/', ProductsListAPIView.as_view(), name='products-list'),
    path('v1/product-statistics/', ProductsStatisticsListAPIView.as_view(), name='product-statistics'),
    path('v1/product/<int:id>/lessons/', ProductLessonsListAPIView.as_view(), name='product-lessons'),
    path('v1/product/<int:id>/students/', ProductStudentsListAPIView.as_view(), name='product-students'),
    path('v1/groups-fullness/', GroupFullnessListAPIView.as_view(), name='groups-fullness'),
]

