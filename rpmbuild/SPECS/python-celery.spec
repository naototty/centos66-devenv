%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%endif

Name:           python-celery
## celery-3.1.17.tar.gz
## Version:        2.2.8
Version:        3.1.17
Release:        3%{?dist}
Summary:        Distributed Task Queue

Group:          Development/Languages
License:        BSD
URL:            http://celeryproject.org
Source0:        http://pypi.python.org/packages/source/c/celery/celery-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       python-anyjson
Requires:       pytz
Requires:       python-amqp
Requires:       python-dateutil15
Requires:       python-kombu
Requires:       pyparsing
%if ! (0%{?fedora} > 13 || 0%{?rhel} > 6)
Requires:       python-importlib
%endif
%if ! (0%{?fedora} > 13 || 0%{?rhel} > 5)
Requires:       python-multiprocessing
Requires:       python-uuid
%endif

%description
An open source asynchronous task queue/job queue based on
distributed message passing. It is focused on real-time
operation, but supports scheduling as well.

The execution units, called tasks, are executed concurrently
on one or more worker nodes using multiprocessing, Eventlet
or gevent. Tasks can execute asynchronously (in the background)
or synchronously (wait until ready).

Celery is used in production systems to process millions of
tasks a day.

Celery is written in Python, but the protocol can be implemented
in any language. It can also operate with other languages using
webhooks.

The recommended message broker is RabbitMQ, but limited support
for Redis, Beanstalk, MongoDB, CouchDB and databases
(using SQLAlchemy or the Django ORM) is also available.

%prep
%setup -q -n celery-%{version}
## [root@dev-iso-upload01 SPECS]# ls ../BUILD/celery-3.1.17/celery/bin/
## amqp.py  base.py  beat.py  celeryd_detach.py  celery.py  events.py  graph.py  __init__.py  multi.py  worker.py
## [root@dev-iso-upload01 SPECS]# ls ../BUILD/celery-3.1.17/celery/app
## amqp.py  annotations.py  base.py  builtins.py  control.py  defaults.py  __init__.py  log.py  registry.py  routes.py  task.py  trace.py  utils.py
## [root@dev-iso-upload01 SPECS]# ls ../BUILD/celery-3.1.17/celery/apps
## beat.py  __init__.py  worker.py
## [root@dev-iso-upload01 SPECS]# 

## for script in celery/bin/camqadm.py celery/bin/celerybeat.py celery/bin/celeryd.py; do
##   %%{__sed} -i.orig -e 1d ${script}
##   touch -r ${script}.orig ${script}
##   %%{__rm} ${script}.orig
##   chmod a-x ${script} 
## done
rm -f docs/.static/.keep

%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
## [root@dev-iso-upload01 SPECS]# ls ../BUILD/celery-3.1.17/
## build  celery  celery.egg-info  Changelog  CONTRIBUTORS.txt  debugfiles.list  debuglinks.list  debugsources.list  docs  examples  extra  LICENSE  MANIFEST.in  PKG-INFO  README.rst  requirements  setup.cfg  setup.py  TODO
## [root@dev-iso-upload01 SPECS]# ls ../BUILD/celery-3.1.17/docs/
## AUTHORS.txt    community.rst      conf.py           copyright.rst  _ext     getting-started  history  includes   internals  reference  templates  _theme     userguide         whatsnew-3.0.rst
## changelog.rst  configuration.rst  contributing.rst  django         faq.rst  glossary.rst     images   index.rst  Makefile   sec        THANKS     tutorials  whatsnew-2.5.rst  whatsnew-3.1.rst
## [root@dev-iso-upload01 SPECS]# ls ../BUILD/celery-3.1.17/examples/
## app  celery_http_gateway  django  eventlet  gevent  httpexample  next-steps  README.rst  resultgraph  tutorial
## [root@dev-iso-upload01 SPECS]# ls ../BUILD/celery-3.1.17/extra/
## bash-completion  centos  generic-init.d  osx  supervisord  systemd  zsh-completion

##%%doc AUTHORS LICENSE README THANKS TODO docs examples
##%%doc docs/AUTHORS.txt docs/community.rst docs/conf.py docs/copyright.rst docs/getting-started docs/history docs/includes docs/internals docs/reference docs/templates docs/userguide docs/whatsnew-3.0.rst docs/changelog.rst
##%%doc docs/configuration.rst docs/contributing.rst docs/django docs/faq.rst docs/glossary.rst docs/images docs/_ext docs/index.rst docs/sec docs/THANKS docs/tutorials docs/whatsnew-2.5.rst docs/whatsnew-3.1.rst
%doc LICENSE README.rst requirements Changelog CONTRIBUTORS.txt TODO docs examples extra
%{python_sitelib}/*
%{_bindir}/*


%changelog
* Fri Feb 20 2015 Naoto Gohko <naoto-gohko@gmo.jp> - 3.1.17-3
- require add : pytz, python-amqp

* Tue Feb 09 2015 Naoto Gohko <naoto-gohko@gmo.jp> - 3.1.17-2
- update 3.1.17

* Wed Oct 09 2013 Matthias Runge <mrunge@redhat.com> - 2.2.8-2
- require python-dateutil15 (rhbz#1002787)

* Mon Nov 28 2011 Andrew Colin Kissa <andrew@topdog.za.net> - 2.2.8-1
- Security FIX CELERYSA-0001

* Fri Jul 15 2011 Andrew Colin Kissa <andrew@topdog.za.net> - 2.2.7-3
- Fix rpmlint errors
- Fix dependencies

* Sat Jun 25 2011 Andrew Colin Kissa <andrew@topdog.za.net> 2.2.7-2
- Update for RHEL6

* Tue Jun 21 2011 Andrew Colin Kissa <andrew@topdog.za.net> 2.2.7-1
- Initial package
