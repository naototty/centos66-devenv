%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)" 2>/dev/null)}

%endif

%define orig_name billiard
%global srcname billiard

## billiard-3.3.0.19.tar.gz
Name:           python-%{srcname}
## Version:        0.3.1
Version:        3.3.0.19
Release:        3%{?dist}
Summary:        Multiprocessing Pool Extensions

Group:          Development/Languages
License:        BSD
URL:            http://pypi.python.org/pypi/billiard
Source0:        http://pypi.python.org/packages/source/b/%{srcname}/%{srcname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
## BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-setuptools


%description
This package contains extensions to the multiprocessing Pool.


%prep
%setup -q -n %{srcname}-%{version}


%build
%{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}

 
%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
## cp: cannot stat `AUTHORS': No such file or directory
## cp: cannot stat `Changelog': No such file or directory
## cp: cannot stat `LICENSE': No such file or directory
## cp: cannot stat `README': No such file or directory
## cp: cannot stat `TODO': No such file or directory
## cp: cannot stat `docs/': No such file or directory
## %%doc AUTHORS Changelog LICENSE README TODO docs/
# ls ../BUILD/billiard-3.3.0.19
# billiard  billiard.egg-info  build  CHANGES.txt  debugfiles.list  debuglinks.list  debugsources.list  Doc  funtests  INSTALL.txt  LICENSE.txt  Makefile  MANIFEST.in  Modules  PKG-INFO  README.rst  requirements  setup.cfg  setup.py
%doc CHANGES.txt Doc funtests INSTALL.txt LICENSE.txt Modules PKG-INFO README.rst requirements setup.cfg setup.py
##%%{python_sitelib}/%%{orig_name}/
%{python_sitearch}/%{orig_name}/
## billiard-3.3.0.19-py2.6.egg-info
##%%{python_sitelib}/%%{orig_name}*.egg-info
%{python_sitearch}/%{orig_name}*.egg-info

%{python_sitearch}/_billiard.so
%{python_sitearch}/funtests/__init__.py
%{python_sitearch}/funtests/__init__.pyc
%{python_sitearch}/funtests/__init__.pyo
%{python_sitearch}/funtests/setup.py
%{python_sitearch}/funtests/setup.pyc
%{python_sitearch}/funtests/setup.pyo

## error: Installed (but unpackaged) file(s) found:
##    /usr/lib/debug/.build-id/99/bbdec29d9f3cb5aff41f98f53c2ae2a595fc4d
##    /usr/lib/debug/.build-id/99/bbdec29d9f3cb5aff41f98f53c2ae2a595fc4d.debug
##    /usr/lib/debug/usr/lib64/python2.6/site-packages/_billiard.so.debug
##    /usr/lib64/python2.6/site-packages/_billiard.so
##    /usr/lib64/python2.6/site-packages/funtests/__init__.py
##    /usr/lib64/python2.6/site-packages/funtests/__init__.pyc
##    /usr/lib64/python2.6/site-packages/funtests/__init__.pyo
##    /usr/lib64/python2.6/site-packages/funtests/setup.py
##    /usr/lib64/python2.6/site-packages/funtests/setup.pyc
##    /usr/lib64/python2.6/site-packages/funtests/setup.pyo
##    /usr/src/debug/billiard-3.3.0.19/Modules/_billiard/connection.h
##    /usr/src/debug/billiard-3.3.0.19/Modules/_billiard/multiprocessing.c
##    /usr/src/debug/billiard-3.3.0.19/Modules/_billiard/multiprocessing.h
##    /usr/src/debug/billiard-3.3.0.19/Modules/_billiard/semaphore.c
##    /usr/src/debug/billiard-3.3.0.19/Modules/_billiard/socket_connection.c

## %%dir /usr/lib/debug
## %%dir /usr/lib/debug/.build-id
## %%dir /usr/lib/debug/.build-id/99
## %%dir /usr/lib/debug/usr
## %%dir /usr/lib/debug/usr/lib64
## %%dir /usr/lib/debug/usr/lib64/python2.6
## %%dir /usr/lib/debug/usr/lib64/python2.6/site-packages
## /usr/lib/debug/.build-id/99/bbdec29d9f3cb5aff41f98f53c2ae2a595fc4d.debug
## /usr/lib/debug/.build-id/99/bbdec29d9f3cb5aff41f98f53c2ae2a595fc4d
## /usr/lib/debug/usr/lib64/python2.6/site-packages/_billiard.so.debug
## /usr/src/debug/billiard-3.3.0.19
## 


%changelog
* Wed Feb 18 2015 Naoto Gohko <naoto-gohko@gmo.jp> - 3.3.0.19-3
- update pkg ; 3.3.0.19-3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Aug 14 2010 Fabian Affolter <fabian@bernewireless.net> - 0.3.1-2
- TODO removed

* Sat Jul 03 2010 Fabian Affolter <fabian@bernewireless.net> - 0.3.1-1
- Initial package
