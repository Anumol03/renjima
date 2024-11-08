"""
URL configuration for new project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from myapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', user_registration, name='user-registration'),
    path('api/users/<int:user_id>/', user_detail, name='user-detail'), 
    path('api/users/<int:user_id>/edit/', user_edit, name='user-edit'),
    path('api/users/<int:user_id>/delete/', user_delete, name='user-delete'), 
    path('api/login/', login_view, name='login'),


    path('api/companies/create/', company_create, name='company-create'),
    path('api/companies/', company_list, name='company-list'), 
    path('api/companies/<int:pk>/edit/', company_edit, name='company-edit'),
    path('api/companies/<int:pk>/deatail/', company_detail, name='company-detail'),
    path('api/companies/<int:pk>/delete/', company_delete, name='company-delete'), 

    path('categories/create/', category_create, name='category-create'),
    path('categories/list/', category_list, name='category-list'),
    path('category/<int:pk>/edit/', category_edit, name='category-edit'),
    path('category/<int:pk>/detail/', category_detail, name='category_detail'),
    path('category/<int:pk>/delete/', category_delete, name='category_delete'),


    path('company/category/list/', list_categories_and_companies, name='list-categories-and-companies'),
    
    
    path('products/create/<int:company_id>/', create_product, name='create_product'),
    path('products/company/<int:company_id>/', list_products, name='list_products_by_company'),
    path('api/products/', list_products1, name='list_products'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),


    path('companies/category/<int:category_id>/', companies_by_category, name='companies-by-category'),
    path('products/category/<int:category_id>/company/<int:company_id>/', products_by_company_and_category, name='products-by-company-and-category'),

    path('product/<int:product_id>/add_to_favorites/', add_to_favorites, name='add_to_favorites'),
    path('user/<int:user_id>/favorites/', list_user_favorites, name='list_user_favorites'),
 

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


