from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('products/',views.products,name = "products"),
<<<<<<< HEAD
    path('subproducts/<str:product_name>/',views.subproducts,name = "subproducts"),
    path('productdetails',views.productdetails,name = "productdetails"),
=======
    path('products/<str:product_name>/',views.subproducts,name = "subproducts"),
>>>>>>> 641dbff8579a3d830047eea54e7cc9a7d275b11d
]