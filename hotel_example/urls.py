from django.conf.urls import url
from hotel_example import views

api_urlpatterns = [
    url(r'^login/$',
        views.LoginAPIView.as_view(),
        name='login'),
    url(r'^user/token/$',
        views.RefreshTokenAPIView.as_view(),
        name='refresh_token'),
    url(r'^users/$',
        views.UsersAPIView.as_view(),
        name='users'),
    url(r'^user/id/(?P<user_id>)/$',
        views.UsersAPIView.as_view(),
        name='user'),
    url(r'^user/profile/$',
        views.ProfileAPIView.as_view(),
        name='profile'),
]
