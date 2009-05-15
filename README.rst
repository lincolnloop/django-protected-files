Install
-------

* ``python setup.py install``

Usage
-----

* add ``protected_files`` to your ``INSTALLED_APPS``
* add an URL to your protected resource to your ``urls.py`` (see ``tests.urls`` for examples)
* configure your static server

Static Server Configuration
---------------------------

Nginx
^^^^^

Place this in your Nginx configuration::

    # this location will only be used by your Django application server
    location /protected {
        internal;
        alias   /protected/files/path/;
    }
    
To Do
-----

* Support alternative means of authorization (user, group, is_staff, etc.)
* Support additional static servers (Lighttpd)