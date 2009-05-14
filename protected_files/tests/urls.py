from django.http import HttpResponse
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^perms/(?P<file_path>.*)', 'protected_files.views.protected_file', {'perm':'auth.add_user'}),
    url(r'^alt-root/(?P<file_path>.*)', 'protected_files.views.protected_file', {'perm':'auth.add_user', 'redirect_root': '/alt/root/path'}),
    url(r'^no-perms/(?P<file_path>.*)', 'protected_files.views.protected_file'),
    
)
