
from favourites.views import FavouriteView
from products.views import ProductView
from substitutes.views import SubstituteView
from django.contrib import admin

from django.urls import path, re_path

from core.views import index, legal_notice
from users.views import (RegisterView, ProfileView,
                         CustomLoginView, CustomLogoutView, custom_logout)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('legal_notice/', legal_notice, name="legal_notice"),
    path('login/', CustomLoginView.as_view(template_name='users/login.html'),
         name='login'),
    path('logout/', custom_logout, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    re_path('^substitute/$', SubstituteView.as_view(), name='substitute'),
    path(r'product/<int:barcode>/', ProductView.as_view(), name='product'),
    path('favourites/', FavouriteView.as_view(), name='favourite')

]
