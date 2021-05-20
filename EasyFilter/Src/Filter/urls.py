from django.urls import path
from Filter.views import home_view, download_view

urlpatterns = [
    path('', home_view, name='home-view'),
    path('download', download_view, name='download-view')
]