# Check for status of man pages
# http://code.google.com/p/redis/issues/detail?id=202

Name:             redis
## redis-2.8.19.tar.gz
## Version:          2.4.10
Version:          2.8.19
Release:          1%{?dist}
Summary:          A persistent key-value database

Group:            Applications/Databases
License:          BSD
URL:              http://redis.io
Source0:          http://redis.googlecode.com/files/%{name}-%{version}.tar.gz
Source1:          %{name}.logrotate
Source2:          %{name}.init
# Update configuration
Patch0:           %{name}-2.4.8-redis.conf.patch
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    tcl >= 8.5

ExcludeArch:      ppc64

Requires:         logrotate
Requires(post):   chkconfig
Requires(postun): initscripts
Requires(pre):    shadow-utils
Requires(preun):  chkconfig
Requires(preun):  initscripts

%description
Redis is an advanced key-value store. It is similar to memcached but the data
set is not volatile, and values can be strings, exactly like in memcached, but
also lists, sets, and ordered sets. All this data types can be manipulated with
atomic operations to push/pop elements, add/remove elements, perform server side
union, intersection, difference between sets, and so forth. Redis supports
different kind of sorting abilities.

%prep
%setup -q
##%%patch0 -p1

%build
make %{?_smp_mflags} \
  DEBUG='' \
  CFLAGS='%{optflags}' \
  V=1 \
  all

%check
make test

%install
rm -fr %{buildroot}
make install PREFIX=%{buildroot}%{_prefix}
# Install misc other
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}
install -p -D -m 644 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}.conf
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{name}
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{name}

# Fix non-standard-executable-perm error
chmod 755 %{buildroot}%{_bindir}/%{name}-*

# Ensure redis-server location doesn't change
mkdir -p %{buildroot}%{_sbindir}
mv %{buildroot}%{_bindir}/%{name}-server %{buildroot}%{_sbindir}/%{name}-server
mv %{buildroot}%{_bindir}/%{name}-sentinel %{buildroot}%{_sbindir}/%{name}-sentinel

## + /bin/mkdir -p /root/rpmbuild/BUILDROOT/redis-2.8.19-1.el6.x86_64/usr/share/doc/redis-2.8.19
## + cp -pr 00-RELEASENOTES BUGS CONTRIBUTING COPYING README INSTALL tests utils /root/rpmbuild/BUILDROOT/redis-2.8.19-1.el6.x86_64/usr/share/doc/redis-2.8.19
## + exit 0
## error: Symlink points to BuildRoot: /usr/bin/redis-sentinel -> /root/rpmbuild/BUILDROOT/redis-2.8.19-1.el6.x86_64/usr/bin/redis-server
## 
## RPM build errors:
##     Symlink points to BuildRoot: /usr/bin/redis-sentinel -> /root/rpmbuild/BUILDROOT/redis-2.8.19-1.el6.x86_64/usr/bin/redis-server


%clean
rm -fr %{buildroot}

%post
/sbin/chkconfig --add redis

%pre
getent group redis &> /dev/null || groupadd -r redis &> /dev/null
getent passwd redis &> /dev/null || \
useradd -r -g redis -d %{_sharedstatedir}/redis -s /sbin/nologin \
-c 'Redis Server' redis &> /dev/null
exit 0

%preun
if [ $1 = 0 ]; then
  /sbin/service redis stop &> /dev/null
  /sbin/chkconfig --del redis &> /dev/null
fi

%files
%defattr(-,root,root,-)
##%%doc 00-RELEASENOTES BUGS CONTRIBUTING COPYING README TODO
## [root@dev-iso-upload01 SPECS]# ls ../BUILD/redis-2.8.19/
## 00-RELEASENOTES  BUGS  CONTRIBUTING  COPYING  deps  INSTALL  Makefile  MANIFESTO  README  redis.conf  runtest  runtest-sentinel  sentinel.conf  src  tests  utils

%doc 00-RELEASENOTES BUGS CONTRIBUTING COPYING README INSTALL tests utils
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.conf
%dir %attr(0755, redis, root) %{_localstatedir}/lib/%{name}
%dir %attr(0755, redis, root) %{_localstatedir}/log/%{name}
%dir %attr(0755, redis, root) %{_localstatedir}/run/%{name}
%{_bindir}/%{name}-*
%{_sbindir}/%{name}-*
%{_initrddir}/%{name}

%changelog
* Fri Feb 20 2015 Naoto Gohko <naoto-gohko@gmo.jp> - 2.8.19-1
- Update to redis 2.8.19

* Sat Mar 31 2012 Silas Sewell <silas@sewell.org> - 2.4.10-1
- Update to redis 2.4.10

* Fri Feb 24 2012 Silas Sewell <silas@sewell.org> - 2.4.8-2
- Disable ppc64 for now
- Enable verbose builds

* Fri Feb 24 2012 Silas Sewell <silas@sewell.org> - 2.4.8-1
- Update to redis 2.4.8

* Sat Apr 23 2011 Silas Sewell <silas@sewell.ch> - 2.2.5-2
- Remove google-perftools-devel

* Sat Apr 23 2011 Silas Sewell <silas@sewell.ch> - 2.2.5-1
- Update to redis 2.2.5

* Tue Oct 19 2010 Silas Sewell <silas@sewell.ch> - 2.0.3-1
- Update to redis 2.0.3

* Fri Oct 08 2010 Silas Sewell <silas@sewell.ch> - 2.0.2-1
- Update to redis 2.0.2
- Disable checks section for el5

* Fri Sep 11 2010 Silas Sewell <silas@sewell.ch> - 2.0.1-1
- Update to redis 2.0.1

* Sat Sep 04 2010 Silas Sewell <silas@sewell.ch> - 2.0.0-1
- Update to redis 2.0.0

* Thu Sep 02 2010 Silas Sewell <silas@sewell.ch> - 1.2.6-3
- Add Fedora build flags
- Send all scriplet output to /dev/null
- Remove debugging flags
- Add redis.conf check to init script

* Mon Aug 16 2010 Silas Sewell <silas@sewell.ch> - 1.2.6-2
- Don't compress man pages
- Use patch to fix redis.conf

* Tue Jul 06 2010 Silas Sewell <silas@sewell.ch> - 1.2.6-1
- Initial package
