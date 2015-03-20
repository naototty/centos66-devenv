
%if 0%{?rhel} && 0%{?rhel} <= 7
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%else
%global with_python3 0
%endif

%global srcname furl

Name:           python-%{srcname}
## ../SOURCES/furl-0.4.4.tar.gz
## ecdsa-0.13.tar.gz
## Version:        0.11
Version:        0.4.4
Release:        3%{?dist}
Summary:        URL manipulation made simple

License:        MIT
URL:            https://pypi.python.org/pypi/ecdsa
# Remove the prime192v1 and secp224r1 curves for now
# https://bugzilla.redhat.com/show_bug.cgi?id=1067697
##############Source0:        %{srcname}-%{version}-clean.tar.gz
Source0:        https://pypi.python.org/packages/source/e/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-six
# For tests
BuildRequires:  openssl
Requires:       python-six

%description
furl is a small Python library that makes manipulating URLs simple.
Python's standard urllib and urlparse modules provide a number of 
URL manipulation functions, but using these functions 
to perform common URL manipulations proves tedious. 
Furl makes manipulating URLs easy.

Furl is well tested, Unlicensed in the public domain, 
and supports both Python 2 and 3.

Query arguments are easy. Really easy.



%prep
##%%setup -q -n %%{srcname}-%%{version}-clean
%setup -q -n %{srcname}-%{version}
rm -rf %{srcname}.egg-info
# Remove extraneous #!
# find ecdsa -name \*.py | xargs sed -ie '/\/usr\/bin\/env/d'
# Use system python-six
# find -name \*.py | xargs sed -ie 's/from \(ecdsa\|\)\.six/from six/g'
# rm ecdsa/six.py



%build
%{__python2} setup.py build



%install

%{__python2} setup.py install --skip-build --root %{buildroot}


%check
echo %{__python2}
## %{__python2} setup.py test
## 

 
%files
# [root@dev-iso-upload01 SPECS]# ls /root/rpmbuild/BUILD/furl-0.4.4/
# build  furl  furl.egg-info  PKG-INFO  setup.cfg  setup.py  tests

%doc PKG-INFO tests
%{python2_sitelib}/*



%changelog
* Thu Mar 12 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-3
- pkg 1st build: 0.4.4

