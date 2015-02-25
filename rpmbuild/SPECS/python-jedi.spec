%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%global srcname jedi

Name:           python-%{srcname}
## ecdsa-0.13.tar.gz
## https://pypi.python.org/packages/source/j/jedi/jedi-0.8.1.tar.gz
## Version:        0.11
## Version:        3.2.6
Version:        0.8.1
## https://pypi.python.org/packages/source/s/subprocess32/subprocess32-3.2.6.tar.gz#md5=754c5ab9f533e764f931136974b618f1
Release:        1%{?dist}
Summary:        backport of the subprocess standard library module python3

License:        MIT
URL:            https://pypi.python.org/pypi/jedi
# Remove the prime192v1 and secp224r1 curves for now
# https://bugzilla.redhat.com/show_bug.cgi?id=1067697
##############Source0:        %%{srcname}-%{version}-clean.tar.gz
Source0:        https://pypi.python.org/packages/source/e/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-six
# For tests
Requires:       python-six

%description
Jedi is an autocompletion tool for Python that can be used in IDEs/editors. 
Jedi works. Jedi is fast. It understands all of the basic Python syntax elements 
including many builtin functions.
Additionaly, Jedi suports two different goto functions and has support 
for renaming as well as Pydoc support and some other IDE features.

Jedi uses a very simple API to connect with IDE’s. 
There’s a reference implementation as a VIM-Plugin, 
which uses Jedi’s autocompletion. 
I encourage you to use Jedi in your IDEs. 
It’s really easy. If there are any problems (also with licensing), ijust contact me.



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
%doc AUTHORS.txt CHANGELOG.rst conftest.py docs jedi LICENSE.txt MANIFEST.in PKG-INFO pytest.ini README.rst sith.py test 
## (devel)[root@dev-iso-upload01 SPECS]# ls ../BUILD/jedi-0.8.1/
## AUTHORS.txt  build  CHANGELOG.rst  conftest.py  docs  jedi  jedi.egg-info  LICENSE.txt  MANIFEST.in  PKG-INFO  pytest.ini  README.rst  setup.cfg  setup.py  sith.py  test  tox.ini


%{python2_sitelib}/*
##%%{python2_sitearch}/*



%changelog
* Wed Feb 25 2015 Naoto Gohko <naoto-gohko@gmo.jp> - 0.8.1-1
- build version: 0.8.1

