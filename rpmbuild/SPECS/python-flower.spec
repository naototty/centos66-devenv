%define pkg_name flower

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%endif

## https://pypi.python.org/pypi/flower

Name:           python-flower
Version:        0.7.3
## https://pypi.python.org/packages/source/f/flower/flower-0.7.3.tar.gz
Release:        1%{?dist}
Summary:        Distributed Task Queue GUI and API management

Group:          Development/Languages
License:        BSD
URL:            http://celeryproject.org
Source0:        https://pypi.python.org/packages/source/f/flower/%{pkg_name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-celery
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

Celery/flower is used in production systems to process millions of
tasks a day.

Celery/flower is written in Python, but the protocol can be implemented
in any language. It can also operate with other languages using
webhooks.

The recommended message broker is RabbitMQ, but limited support
for Redis, Beanstalk, MongoDB, CouchDB and databases
(using SQLAlchemy or the Django ORM) is also available.

%prep
%setup -q -n %{pkg_name}-%{version}
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
# [root@dev-iso-upload01 SPECS]# ls ../BUILD/flower-0.7.3/
# AUTHORS  build  CHANGES  docs  flower  flower.egg-info  LICENSE  MANIFEST.in  PKG-INFO  README.rst  setup.cfg  setup.py  tests

%doc LICENSE README.rst AUTHORS docs PKG-INFO tests
%{python_sitelib}/*
%{_bindir}/*


%changelog
* Tue Mar 10 2015 Naoto Gohko <naoto-gohko@gmo.jp> - 0.7.3-1
- update 0.7.3
