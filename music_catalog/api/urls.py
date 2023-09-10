from django.urls import path, include
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import MusicianViewSet, AdminLoginView, SongViewSet, AlbumViewSet

router = routers.DefaultRouter()
router.register(r'musicians', MusicianViewSet, basename='musicians')
router.register(
    (album_url := r'musicians/(?P<musician>[^/.]+)/albums'),
    AlbumViewSet, basename='albums'
)
router.register(
    album_url + r'/(?P<album>[^/.]+)/songs',
    SongViewSet, basename='songs'
)

urlpatterns = [
    path('v1/login/', AdminLoginView.as_view(), name='login'),
    path('v1/', include(router.urls)),
    path(
        'v1/schema/',
        SpectacularAPIView.as_view(),
        name='schema'
    ),
    path(
        'v1/swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger'
    ),
]
