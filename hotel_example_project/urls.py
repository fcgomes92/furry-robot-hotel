from django.conf.urls import url, include
from django.contrib import admin
from hotel_example import urls as hotel_example_urls

urlpatterns = [
    url(r'^api/v1/',
        include(hotel_example_urls.api_urlpatterns,
                namespace='hotel_example_api')),
]
