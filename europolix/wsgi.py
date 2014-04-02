"""
WSGI config for europolix project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.
"""

#encoding error (production server only)
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#add the current directory to python path
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "europolix.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
#~ import sys
#~ path=os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
#~ if path not in sys.path:
    #~ sys.path.append(path)
    #~ sys.path.append( os.path.join( path, appname) )
#~ os.environ['DJANGO_SETTINGS_MODULE']=appname+'.settings'
import django.core.handlers.wsgi
#~ from django.core.wsgi import get_wsgi_application
application=django.core.handlers.wsgi.WSGIHandler()
