from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('products/',views.products,name = "products"),
    path('products/<str:product_name>/',views.subproducts,name = "subproducts"),
    path('products/<str:product_name>/<str:product_details>/',views.productdetails,name = "productdetails"),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact")
]