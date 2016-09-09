from django.conf.urls import url
from hotel_example import views

api_urlpatterns = [
    url(r'^users/$', views.UsersAPIView.as_view(), name='users'),
    url(r'^users/id/(?P<user_id>)/$', views.UsersAPIView.as_view(),
        name='user'),
    url(r'^profile/$', views.ProfileAPIView.as_view(), name='profile'),
]
