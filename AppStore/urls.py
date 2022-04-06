"""AppStore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import app.views


urlpatterns = [
    path('admin/', app.views.admin_users, name='admin user'),
    path('admin/admin_user_edit/<int:id>', app.views.admin_users_edit, name='admin_user_edit'),
    path('admin/admin_product/', app.views.admin_product, name='admin_product'),
    path('admin/admin_product_edit/<int:id>/', app.views.admin_product_edit, name='admin_product_edit'),
    path('', app.views.home, name='home'),
    path('register/', app.views.register, name='register'),
    path('profile/<str:id>', app.views.profile, name='profile'),
    path('login/', app.views.signin, name='login'),
    path('logout/', app.views.signout, name='logout'),
    path('view/<int:id>', app.views.view, name='view'),
    path('view/purchase/<int:id>', app.views.user_purchase, name='purchase'),
    path('view/home', app.views.purchase_more, name='purchasemore'),
    path('sell_something/', app.views.sell, name="sell"),
    path('search_products/', app.views.search_products, name='search_products'),
    path('search_users/', app.views.search_users, name='search_users')
    
]


