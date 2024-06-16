from django.urls import path,include
from rest_framework.authtoken.views import obtain_auth_token

from  api import views

app_name = 'api'

urlpatterns = [
    # POST/DELETE URLS
    path('<slug:category_slug>/assets/<slug:asset_slug>/transaction/delete/<int:transaction_id>/', views.remove_asset_transaction, name='remove_asset_transaction'),
    path('<slug:category_slug>/assets/<slug:asset_slug>/transaction/', views.asset_transaction_view, name='add_asset_transaction'),
    path('<slug:category_slug>/assets/create/', views.create_new_asset, name='create_new_asset'),
    # GET URLS
    path('api-token-auth/', obtain_auth_token, name='get_user_api_token'),
    path('categories/', views.all_categories, name='all_categories'),
    path('<slug:category_slug>/assets/', views.category_asset_listing_view, name='all_category_assets_listing'),
    path('<slug:category_slug>/assets/<slug:asset_slug>/delete/', views.remove_category_asset, name='remove_category_asset'),
    path('<slug:category_slug>/assets/<slug:asset_slug>/', views.asset_detail_view, name='asset_detail'),
]