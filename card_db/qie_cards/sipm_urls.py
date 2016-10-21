from django.conf.urls import url, include
from django.views.static import serve

from . import sipm_views as views
from card_db.settings import MEDIA_ROOT

urlpatterns = [
    #url(r'^catalog$', views.CatalogView.as_view(), name='catalog'),
    url(r'^catalog$', views.catalog, name='catalog'),
    url(r'^(?P<sipm_control_card>[0-9]{1,4})/$', views.detail, name='detail'),
    ]
