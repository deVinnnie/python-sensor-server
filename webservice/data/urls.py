from django.conf.urls import patterns, url
from django.conf import settings
from data import views

urlpatterns = patterns('',
    url (
        regex = r'^alerts$',
        view = views.alerts,
        name = 'alerts'
    )
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
