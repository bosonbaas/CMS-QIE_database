from django.conf.urls import url, include
from django.views.static import serve

from . import rm_views as views
from card_db.settings import MEDIA_ROOT

urlpatterns = [
    #url(r'^catalog$', views.CatalogView.as_view(), name='catalog'),
    url(r'^catalog$', views.catalog, name='catalog'),
    url(r'^(?P<rm>[0-9]{1,4})/$', views.detail, name='detail'),
    url(r'^uid/(?P<rm>[a-fA-F0-9_]{6,27})/$', views.detail, name='detail'),
    url(r'^error$', views.error, name='error'),
    ]
