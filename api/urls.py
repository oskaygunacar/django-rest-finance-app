from django.urls import path,include
from rest_framework.authtoken.views import obtain_auth_token

from  api import views

app_name = 'api'

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='get_user_api_token'),
    path('categories/', views.all_categories, name='all_categories'),
    path('<slug:category_slug>/assets/', views.category_asset_listing_view, name='all_category_assets_listing'),
]