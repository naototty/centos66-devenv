
%if 0%{?rhel} && 0%{?rhel} <= 7
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%else
%global with_python3 0
%endif

%global srcname orderedmultidict

Name:           python-%{srcname}
## orderedmultidict-0.7.4.tar.gz
## ../SOURCES/furl-0.4.4.tar.gz
## ecdsa-0.13.tar.gz
## Version:        0.11
Version:        0.7.4
Release:        3%{?dist}
Summary:        Ordered Multivalue Dictionary - omdict.

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
A multivalue dictionary is a dictionary that can store multiple values for the same key. 
An ordered multivalue dictionary is a multivalue dictionary that retains 
the order of insertions and deletions.

omdict retains method parity with dict.

Information and documentation at https://github.com/gruns/orderedmultidict.



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

%doc PKG-INFO tests
%{python2_sitelib}/*



%changelog
* Thu Mar 12 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-3
- pkg 1st build: 0.7.4

