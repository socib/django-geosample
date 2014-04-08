..

django-geosample
======================

Introduction
------------

This is a dummy django project using `geodjango <http://geodjango.org/>`_, following the structure proposed in this `django best practices guide <http://lincolnloop.com/django-best-practices/index.html>`_ from Lincoln Loop.


Requirements
------------

This project includes bootstrap less files, which are compiled into css via django-compressor and nodejs package lessc (see `lessc <http://lesscss.org>`_ ). You should install nodejs and lessc from node package manager::

    npm install -g less

You will also need an spatial database (see `geodjango requirements <https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/#requirements>`_ ).


Quickstart
----------

To configure the project in development::

    mkvirtualenv geosample --no-site-packages
    workon geosample
    cd path/to/geosample/repository
    pip install -r requirements.pip
    pip install -e .
    cp geosample/settings/local.py.example geosample/settings/local.py
    python manage.py syncdb
    python manage.py migrate
    python manage.py runserver_plus

