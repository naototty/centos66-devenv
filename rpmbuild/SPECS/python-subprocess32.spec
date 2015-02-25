%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%global srcname subprocess32

Name:           python-%{srcname}
## ecdsa-0.13.tar.gz
## Version:        0.11
Version:        3.2.6
## https://pypi.python.org/packages/source/s/subprocess32/subprocess32-3.2.6.tar.gz#md5=754c5ab9f533e764f931136974b618f1
Release:        1%{?dist}
Summary:        backport of the subprocess standard library module python3

License:        MIT
URL:            https://pypi.python.org/pypi/subprocess32
# Remove the prime192v1 and secp224r1 curves for now
# https://bugzilla.redhat.com/show_bug.cgi?id=1067697
##############Source0:        %{srcname}-%{version}-clean.tar.gz
Source0:        https://pypi.python.org/packages/source/e/%{srcname}/%{srcname}-%{version}.tar.gz

## BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-six
# For tests
Requires:       python-six

%description
This is an This is a backport of the subprocess standard library module from 
Python 3.2 & 3.3 for use on Python 2.4, 2.5, 2.6 and 2.7. 
It includes bugfixes and new features. 
On POSIX systems it is guaranteed to be reliable when used 
in threaded applications. Bonus: It includes timeout support from Python 3.3.
into other protocols.



%prep
##%%setup -q -n %%{srcname}-%%{version}-clean
%setup -q -n %{srcname}-%{version}

rm -rf %{srcname}.egg-info

# Remove extraneous #!
# find %{srcname} -name \*.py | xargs sed -ie '/\/usr\/bin\/env/d'
# Use system python-six
# find %{srcname} -name \*.py | xargs sed -ie 's/from \(ecdsa\|\)\.six/from six/g'
# rm ecdsa/six.py


%build
%{__python2} setup.py build


%install
%{__python2} setup.py install --skip-build --root %{buildroot}


%check
echo %{__python2}
##%%{__python2} setup.py test
 

 
%files
%doc LICENSE ChangeLog PKG-INFO README.txt _posixsubprocess.c _posixsubprocess_helpers.c setup.cfg testdata test_subprocess32.py
## [root@dev-iso-upload01 SPECS]# ls ../BUILD/subprocess32-3.2.6/
## build  ChangeLog  LICENSE  MANIFEST.in  PKG-INFO  _posixsubprocess.c  _posixsubprocess_helpers.c  README.txt  setup.cfg  setup.py  subprocess32.py  testdata  test_subprocess32.py

##%%{python2_sitelib}/*
%{python2_sitearch}/*



%changelog
* Wed Feb 25 2015 Naoto Gohko <naoto-gohko@gmo.jp> - 3.2.6-1
- build version: 3.2.6

