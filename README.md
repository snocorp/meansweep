Meansweep
=========

Simple minesweep clone using Django as the back-end on OpenShift. The front end uses Bootstrap and Angular.

Getting Started
---------------

I used this great [tutorial](https://github.com/rancavil/django-openshift-quickstart/wiki/Tutorial-How-create-an-application-with-Django-1.6-on-Openshift) to get started. See below if you just want to run your own meansweep instance.

1. Install python 2.7
2. Install pip
3. Install sqlite3
4. Run `python setup.py install`
5. In wsgi/openshift run `python manage.py syncdb`
6. In wsgi/openshift run `python manage.py runserver 0.0.0.0:3000`

Attribution
-----------

This application was bootstrapped using 
* https://github.com/rancavil/django-openshift-quickstart
* https://github.com/angular/angular-seed