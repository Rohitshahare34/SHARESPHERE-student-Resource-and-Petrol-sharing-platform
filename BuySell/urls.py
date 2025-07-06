from django.urls import path
from .views import home, sell_product, upload_item
from django.conf import settings
from django.conf.urls.static import static
from .views import add_to_cart, remove_from_cart, profile, edit_profile, add_to_wishlist, remove_from_wishlist
  
from BuySell import views



urlpatterns = [
    path('', views.home, name='buysell_home'),  # Ensure this name matches the URL used in home.html
    path('sell_product/', views.sell_product, name='sell_product'),  # Fixed syntax
    path('upload_item/', views.upload_item, name='upload_item'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/', remove_from_cart, name='remove_from_cart'),
    path('add_to_wishlist/', add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/', remove_from_wishlist, name='remove_from_wishlist'),
    path('profile/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
]
