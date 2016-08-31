from django.conf.urls import url, include
from django.views.static import serve

from . import card_views as views
from card_db.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^catalog$', views.CatalogView.as_view(), name='catalog'),
    url(r'^summary$', views.summary, name='summary'),
    url(r'^testers$', views.TestersView.as_view(), name='testers'),
    url(r'^stats$', views.stats, name='stats'),
    url(r'^test-details$', views.TestDetailsView.as_view(), name='test-details'),
    url(r'^(?P<card>[0-9]{3,7})/$', views.detail, name='detail'),
    url(r'^(?P<card>[0-9]{3,7})/calibration$', views.calibration, name='calibration'),
    url(r'^(?P<card>[0-9]{3,7})/calibration/(?P<group>[0-9]{1,2})/plots$', views.calPlots, name='plotview'),
    url(r'^(?P<card>[0-9]{3,7})/calibration/(?P<group>[0-9]{1,2})/results$', views.calResults, name='results'),
    url(r'^media/(?P<path>.*)$',serve, {'document_root':MEDIA_ROOT}),
    url(r'^plots$', views.PlotView.as_view(), name='plots'),
    url(r'^(?P<card>[0-9]{3,7})/(?P<test>.*)$', views.testDetail, name='testDetail'),
    url(r'^field$', views.fieldView, name='fieldView'),
]
