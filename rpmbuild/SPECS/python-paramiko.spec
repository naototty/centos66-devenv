%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define srcname paramiko

Name:           python-paramiko
## Version:        1.7.5
Version:        1.12.4
Release:        2.1%{?dist}
Summary:        A SSH2 protocol library for python

Group:          Development/Libraries
# No version specified.
License:        LGPLv2+
URL:            http://www.lag.net/paramiko/
Source0:        http://www.lag.net/paramiko/download/%{srcname}-%{version}.tar.gz
Patch0: 	paramiko-channel-race.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

%if 0%{?fedora} >= 8 || 0%{?rhel} >= 6
BuildRequires: python-setuptools-devel
%else
BuildRequires: python-setuptools
%endif

Requires:       python-crypto >= 1.9

%description
Paramiko (a combination of the esperanto words for "paranoid" and "friend") is
a module for python 2.3 or greater that implements the SSH2 protocol for secure
(encrypted and authenticated) connections to remote machines. Unlike SSL (aka
TLS), the SSH2 protocol does not require heirarchical certificates signed by a
powerful central authority. You may know SSH2 as the protocol that replaced
telnet and rsh for secure access to remote shells, but the protocol also
includes the ability to open arbitrary channels to remote services across an
encrypted tunnel. (This is how sftp works, for example.)

%prep
%setup -q -n %{srcname}-%{version}
##%%patch0 -p0 -b .race
%{__chmod} a-x demos/*
##%%{__sed} -i -e '/^#!/,1d' demos/* paramiko/rng*

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} -c 'import setuptools; execfile("setup.py")' build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} -c 'import setuptools; execfile("setup.py")' install --skip-build --root %{buildroot}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE PKG-INFO README docs/ demos/
%{python_sitelib}/*

%changelog
* Fri Feb 20 2015 Naoto Gohko <naoto-gohko@gmo.jp> - 1.12.4-1
- Major version update: 1.12.4

* Fri Nov 13 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.7.5-2.1
- Fix conditional for RHEL

* Tue Oct 13 2009 Jeremy Katz <katzj@fedoraproject.org> - 1.7.5-2
- Fix race condition (#526341)

* Thu Jul 23 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.5-1
- v1.7.5 (Ernest) 19jul09
- -----------------------
-  * added support for ARC4 cipher and CTR block chaining (Denis Bernard)
-  * made transport threads daemonize, to fix python 2.6 atexit behavior
-  * support unicode hostnames, and IP6 addresses (Maxime Ripard, Shikhar
-    Bhushan)
-  * various small bug fixes

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.4-4
- Add demos as documentation. BZ#485742

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.7.4-3
- Rebuild for Python 2.6

* Wed Sep  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.7.4-2
- fix license tag

* Sun Jul  6 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.4-1
- Update to 1.7.4

* Mon Mar 24 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.3-1
- Update to 1.7.3.

* Tue Jan 22 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.2-1
- Update to 1.7.2.
- Remove upstreamed patch.

* Mon Jan 14 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.1-3
- Update to latest Python packaging guidelines.
- Apply patch that fixes insecure use of RandomPool.

* Thu Jul 19 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.1-2
- Bump rev

* Thu Jul 19 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.1-1
- Update to 1.7.1

* Sat Dec 09 2006 Toshio Kuratomi <toshio@tiki-lounge.com> - 1.6.4-1
- Update to 1.6.4
- Upstream is now shipping tarballs
- Bump for python 2.5 in devel

* Mon Oct  9 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.6.2-1
- Update to 1.6.2

* Sat Sep 16 2006 Shahms E. King <shahms@shahms.com> 1.6.1-3
- Rebuild for FC6

* Fri Aug 11 2006 Shahms E. King <shahms@shahms.com> 1.6.1-2
- Include, don't ghost .pyo files per new guidelines

* Tue Aug 08 2006 Shahms E. King <shahms@shahms.com> 1.6.1-1
- Update to new upstream version

* Fri Jun 02 2006 Shahms E. King <shahms@shahms.com> 1.6-1
- Update to new upstream version
- ghost the .pyo files

* Fri May 05 2006 Shahms E. King <shahms@shahms.com> 1.5.4-2
- Fix source line and rebuild

* Fri May 05 2006 Shahms E. King <shahms@shahms.com> 1.5.4-1
- Update to new upstream version

* Wed Apr 12 2006 Shahms E. King <shahms@shahms.com> 1.5.3-1
  - Initial package
