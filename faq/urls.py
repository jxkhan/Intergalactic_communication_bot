from rest_framework.routers import DefaultRouter
from .viewset import CategoriesViewSet, FAQViewSet, CustomerViewSet
from django.urls import path , include 




router= DefaultRouter()
router.register(r'categories', CategoriesViewSet, basename='categories')
router.register(r'faqs', FAQViewSet, basename='faqs')
router.register(r'customers', CustomerViewSet , basename='customers')

urlpatterns=[
    path('', include(router.urls)),
    path('auth/login/', CustomerViewSet.as_view({'post': 'customer_login'}), name='customer-login'),
    path('auth/logout/', CustomerViewSet.as_view({'post': 'customer_logout'}), name='customer-logout'),
]


