from django.conf.urls import url, include
from django.views.static import serve

from . import rm_views as views
from card_db.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^catalog$', views.CatalogView.as_view(), name='catalog'),
    ]
