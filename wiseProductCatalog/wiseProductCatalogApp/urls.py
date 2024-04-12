from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('products/',views.products,name = "products"),
    path('subproducts/<str:product_name>/',views.subproducts,name = "subproducts"),
    path('productdetails',views.productdetails,name = "productdetails"),
]