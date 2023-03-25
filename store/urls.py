from .import views
from django.urls import path

urlpatterns = [
    path('', views.store, name ="store"),
    path('cart/', views.cart, name ="cart"),
    path('checkout/', views.checkout, name ="checkout"),
    path('update_item/', views.UpdateItem, name = "update_item"),
    path('process_order/', views.processorder, name = "process_order"),
    path('profile/', views.profile, name="users-profile"),
]