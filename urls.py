from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from api.views import get_brigades_by_activity

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='index.html'), name="home"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^data/home-page-data/', get_brigades_by_activity),
)
