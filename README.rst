Carona Sustentável
==================

Projeto de um site de caronas pronto para ser hospedado no OpenShift (http://openshift.redhat.com)

Features
--------

* Completely free, thanks to Red Hat's OpenShift Express
* MySQL database automatically setup for your application
* Dynamic database configuration at runtime. No passwords stored in your configs.
* Your application's test suite is run after each push
* Automatic deployment upon git push
* No need to think about servers, let alone apache/mod_wsgi configuration


Monitoring your logs
--------------------

::

    rhc-tail-files -a pyramidapp -l your@email.com
