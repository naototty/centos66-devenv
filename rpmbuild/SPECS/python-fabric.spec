
## GMO Admin tools setting
##%%define __python python26
%define __python python

## Fabric-0.9.0.tar.gz
## Fabric-0.9.1.tar.gz


%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

##Name:           fabric
Name:           python-fabric
##Version:        0.9.0
##Version:        0.9.1
##Version:        0.9.3
##Version:        1.0.1
##Version:        1.0.2
## Version:        1.2.2
Version:        1.8.5
####Release:        3%%{?dist}
####Release:        4%%{?dist}
##Release:        1r2%%{?dist}
Release:        1r8%{?dist}
Summary:        A simple pythonic remote deployment tool

Group:          Applications/System
License:        GPLv2+
URL:            http://www.nongnu.org/fab/
##Source0:        http://download.savannah.gnu.org/releases/fab/fab-%%{version}.tar.gz
##Source0:        http://code.fabfile.org/projects/fabric/files/Fabric-%%{version}.tar.gz
Source0:        http://code.fabfile.org/projects/fabric/files/fabric-%{version}.tar.gz
## http://code.fabfile.org/projects/fabric/files/Fabric-0.9.3.tar.gz
Patch10001:     fabric-1.2.0-unicode.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
#BuildRequires:  python-devel
#BuildRequires:  python-setuptools
#Requires:       python-paramiko >= 1.7
#Requires:       python-setuptools
BuildRequires:  python-devel >= 2.6
BuildRequires:  python-setuptools
##Requires:       python26-paramiko >= 1.7
Requires:       python-paramiko >= 1.10
## Requires:       paramiko >= 1.10
Requires:       python-crypto >= 2.0.1
Requires:       python-setuptools
##
##Provides: python26-paramiko, py26-fabric
##Obsoletes: python26-paramiko, py26-fabric
##Conflicts: python26-paramiko

#Provides: webserver, apache, httpd
#Obsoletes: webserver, apache, httpd
Obsoletes: py26-fabric
#Conflicts: thttpd



%description
Fabric is a simple pythonic remote deployment tool which is designed to upload
files to, and run shell commands on, a number of servers in parallel or
serially.

%prep
##%%setup -q -n fab-%%{version}
##%%setup -q -n Fabric-%%{version}
%setup -q -n fabric-%{version}
## GMO Unicode patch
###########%%patch10001 -p1

##sed -i '/^#!\/usr\/bin\/env\ python -i/,+1 d' fabric.py
sed -i '/^#!\/usr\/bin\/env\ python -i/,+1 d' setup.py

%build
%{__python} setup.py build
%{__python} setup.py test

%install
rm -rf $RPM_BUILD_ROOT

pwd
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
rm -rvf $RPM_BUILD_ROOT%{python_sitelib}/paramiko
##rm -rvf $RPM_BUILD_ROOT%{python_sitelib}/usr/lib/python2.6/site-packages/paramiko


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
###%%doc fabfile.py LICENSE README FAQ INSTALL PKG-INFO docs
%doc LICENSE README.rst INSTALL fabfile sites requirements.txt dev-requirements.txt AUTHORS CONTRIBUTING.rst
## cp: cannot stat `README': No such file or directory
## cp: cannot stat `docs': No such file or directory
## [root@el6boot SPECS]# ls ../BUILD/fabric-1.8.5/
## AUTHORS  CONTRIBUTING.rst  Fabric.egg-info  INSTALL  LICENSE  MANIFEST.in  README.rst  build  debugfiles.list  debuglinks.list  debugsources.list  dev-requirements.txt  fabfile  fabric  integration  requirements.txt  setup.py  sites  tasks.py  tests


%{python_sitelib}/*
%{_bindir}/fab

## [root@el6sg04 SPECS]# ls -l /home/build/repo/master/openstack/redhat/BUILD/fabric-1.2.2/
## 合計 52
## -rw-r--r-- 1 root root  866  9月  2 07:26 2011 AUTHORS
## drwxr-xr-x 2 root root 4096  9月 30 11:16 2011 Fabric.egg-info
## -rw-r--r-- 1 root root  109  9月  2 07:26 2011 INSTALL
## -rw-r--r-- 1 root root 1346  9月  2 07:26 2011 LICENSE
## -rw-r--r-- 1 root root  197  9月  2 07:26 2011 MANIFEST.in
## -rw-r--r-- 1 root root 1258  9月  2 07:26 2011 README
## drwxr-xr-x 3 root root 4096  9月 30 11:16 2011 build
## -rw-r--r-- 1 root root    0  9月 30 11:16 2011 debugfiles.list
## -rw-r--r-- 1 root root    0  9月 30 11:16 2011 debuglinks.list
## -rw-r--r-- 1 root root    0  9月 30 11:16 2011 debugsources.list
## drwxr-xr-x 6 root root 4096  9月  2 07:26 2011 docs
## drwxr-xr-x 2 root root 4096  9月  2 07:26 2011 fabfile
## drwxr-xr-x 3 root root 4096  9月 30 11:16 2011 fabric
## -rw-r--r-- 1 root root  453  9月  2 07:26 2011 requirements.txt
## -rw-r--r-- 1 root root 2082  9月 30 11:16 2011 setup.py
## drwxr-xr-x 3 root root 4096  9月  2 07:26 2011 tests

## [root@boot SPECS]# ls -1 ../BUILD/Fabric-0.9.1/
## AUTHORS
## Fabric.egg-info
## INSTALL
## LICENSE
## MANIFEST.in
## PKG-INFO
## README
## build
## docs
## fabfile.py
## fabric
## paramiko
## requirements.txt
## setup.cfg
## setup.py
## tests
## [root@boot SPECS]# ls -1 ../BUILD/Fabric-0.9.1/docs
## api
## changes
## development.rst
## faq.rst
## index.rst
## installation.rst
## tutorial.rst
## usage
## [root@boot SPECS]# ls -1 ../BUILD/Fabric-0.9.1/tests/
## test_context_managers.py
## test_main.py
## test_network.py
## test_operations.py
## test_state.py
## test_utils.py
## test_version.py
## utils.py


##  [root@boot SPECS]# rpm -Uvh /export/var/src/redhat/RPMS/noarch/py26-fabric-0.9.0-4.noarch.rpm


%changelog
* Fri Feb 20 2015 Naoto Gohko <naoto-gohko@gmo.jp> - 1.8.5-1
- Rebuilt for https://pypi.python.org/packages/source/F/Fabric/Fabric-1.8.5.tar.gz
- Major version update

* Tue Jul 12 2011 Naoto Gohko <naoto-gohko@gmo.jp> - 1.0.2-1
- Rebuilt for http://code.fabfile.org/projects/fabric/files/Fabric-1.0.2.tar.gz
- Major version update

* Tue May 24 2011 Naoto Gohko <naoto-gohko@gmo.jp> - 1.0.1-1
- Rebuilt for http://code.fabfile.org/projects/fabric/files/Fabric-1.0.1.tar.gz
- Major version update

* Wed Dec 22 2010 Naoto Gohko <naoto-gohko@gmo.jp> - 0.9.3-1
- Rebuilt for http://code.fabfile.org/projects/fabric/files/Fabric-0.9.3.tar.gz
- Major version update

* Thu Sep 22 2010 Naoto Gohko <naoto-gohko@gmo.jp> - 0.9.1-1
- Rebuilt for http://code.fabfile.org/projects/fabric/files/Fabric-0.9.1.tar.gz
- Major version update

* Fri Nov 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-3
- Rebuilt for http://code.fabfile.org/projects/fabric/files/Fabric-0.9.0.tar.gz
- Major version update

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 12 2009 Silas Sewell <silas at sewell ch> - 0.1.1-2
- Add runtime setuptools requirements
- Re-import source package

* Thu Apr 09 2009 Silas Sewell <silas at sewell ch> - 0.1.1-1
- Update to 0.1.1
- Up Paramiko version dependency to 1.7
- Remove Python version dependency
- Make sed safer

* Sat Mar 28 2009 Silas Sewell <silas at sewell ch> - 0.1.0-3
- Fix dependencies
- Fix non-executable-script error

* Thu Mar 26 2009 Silas Sewell <silas at sewell ch> - 0.1.0-2
- Changed define to global

* Sun Feb 22 2009 Silas Sewell <silas at sewell ch> - 0.1.0-1
- Updated to 0.1.0
- Upped Python requirement to 2.5 per recommendation on official site

* Thu Nov 20 2008 Silas Sewell <silas at sewell ch> - 0.0.9-3
- Fixed changelog syntax issue

* Thu Nov 20 2008 Silas Sewell <silas at sewell ch> - 0.0.9-2
- Fixed various issues with the SPEC file

* Wed Nov 19 2008 Silas Sewell <silas at sewell ch> - 0.0.9-1
- Initial package
