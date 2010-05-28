import settings

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^website/', include('website.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('main.views',
    (r'^$', 'about'),
    (r'^presets/$', 'presets'),
    (r'^presets/submit/$', 'preset_submit'),
    (r'^presets/create/$', 'preset_create'),
    (r'^screenshots/$', 'screenshots'),
    (r'^downloads/$', 'downloads'),
    (r'^contact/$', 'contact'),
    (r'^contact/thanks/$', 'thanks'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        # serving the admin media
        (r'^media/(?P<path>.*)$', 
            'django.views.static.serve', 
            {'document_root': settings.PROJECT_ROOT + '/media'}),
        (r'^media/admin/(?P<path>.*)$', 
            'django.views.static.serve', 
            {'document_root': settings.PROJECT_ROOT + '/media/admin'}),
    )

