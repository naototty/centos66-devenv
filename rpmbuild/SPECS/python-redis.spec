%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global upstream_name redis

Name:           python-%{upstream_name}
## redis-2.10.3.tar.gz
## Version:        2.0.0
Version:        2.10.3
Release:        1%{?dist}
Summary:        A Python client for redis

Group:          Development/Languages
License:        MIT
URL:            http://github.com/andymccurdy/redis-py
Source0:        http://github.com/downloads/andymccurdy/redis-py/%{upstream_name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel

%description
This is a Python interface to the Redis key-value store.

%prep
%setup -q -n %{upstream_name}-%{version}

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
# [root@dev-iso-upload01 SPECS]# ls ../BUILD/redis-2.10.3/
# build  CHANGES  INSTALL  LICENSE  MANIFEST.in  PKG-INFO  README.rst  redis  redis.egg-info  setup.cfg  setup.py  tests
%defattr(-,root,root,-)
%doc CHANGES LICENSE README.rst INSTALL PKG-INFO tests
%{python_sitelib}/%{upstream_name}
%{python_sitelib}/%{upstream_name}-%{version}-*.egg-info

%changelog
* Sat Sep 04 2010 Silas Sewell <silas@sewell.ch> - 2.0.0-1
- Initial build
