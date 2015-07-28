
##%%define pkg_rel dev22.ss.20140320
###%%define pkg_rel dev26
##%%define pkg_rel g1
%define pkg_rel g2

%define haproxy_user    haproxy
%define haproxy_group   %{haproxy_user}
%define haproxy_home    %{_localstatedir}/lib/haproxy
%define haproxy_confdir %{_sysconfdir}/haproxy
%define haproxy_datadir %{_datadir}/haproxy

Summary: HA-Proxy is a TCP/HTTP reverse proxy for high availability environments
Name: haproxy
## Version: 1.5
## Version: 1.5.10
## Version: 1.5.11
Version: 1.5.14
## Release: 1.dev22
## Release: 1.dev22.ss.20140320
Release: 1.%{pkg_rel}
## haproxy-1.5-dev22-ss-20140320.tar.gz
License: GPL
Group: System Environment/Daemons
URL: http://haproxy.1wt.eu/
## Source0: http://haproxy.1wt.eu/download/1.5/src/devel/%%{name}-%%{version}.tar.gz
## Source0: http://haproxy.1wt.eu/download/1.5/src/devel/%%{name}-%%{version}-dev22.tar.gz
## Source0: http://haproxy.1wt.eu/download/1.5/src/devel/%{name}-%{version}-dev22-ss-20140320.tar.gz
## haproxy-1.5.10.tar.gz
## http://www.haproxy.org/download/1.5/src/haproxy-1.5.10.tar.gz
## Source0: http://haproxy.1wt.eu/download/1.5/src/devel/%%{name}-%%{version}-%{pkg_rel}.tar.gz
Source0: http://www.haproxy.org/download/1.5/src/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-root
## haproxy-1.5-dev22-ss-20140320.tar.gz
BuildRequires: pcre-devel zlib-devel openssl-devel
Requires: /sbin/chkconfig, /sbin/service
Requires(pre):      shadow-utils

%description
HA-Proxy is a TCP/HTTP reverse proxy which is particularly suited for high
availability environments. Indeed, it can:
- route HTTP requests depending on statically assigned cookies
- spread the load among several servers while assuring server persistence
  through the use of HTTP cookies
- switch to backup servers in the event a main one fails
- accept connections to special ports dedicated to service monitoring
- stop accepting connections without breaking existing ones
- add/modify/delete HTTP headers both ways
- block requests matching a particular pattern

It needs very little resource. Its event-driven architecture allows it to easily
handle thousands of simultaneous connections on hundreds of instances without
risking the system's stability.

%prep
##%%setup -q -n %%{name}-%%{version}-dev22-ss-20140320
##%%setup -q -n %{name}-%%{version}-%%{pkg_rel}
%setup -q -n %{name}-%{version}

# We don't want any perl dependecies in this RPM:
%define __perl_requires /bin/true

%build
## ORIG ## %%{__make} USE_PCRE=1 DEBUG="" ARCH=%%{_target_cpu} TARGET=linux26
## for SSL
%{__make} USE_PCRE=1 DEBUG="" USE_OPENSSL=1 USE_ZLIB=1 ADDLIB=-lz ARCH=%{_target_cpu} TARGET=linux26

# build the halog contrib program.
pushd contrib/halog
make ${halog} OPTIMIZE="%{optflags}"
popd

%install
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}
 
%{__install} -d %{buildroot}%{_sbindir}
%{__install} -d %{buildroot}%{_sysconfdir}/rc.d/init.d
%{__install} -d %{buildroot}%{_sysconfdir}/%{name}
%{__install} -d %{buildroot}%{_mandir}/man1/

%{__install} -d -m 0755 %{buildroot}%{haproxy_home}
%{__install} -d -m 0755 %{buildroot}%{haproxy_datadir}

%{__install} -s %{name} %{buildroot}%{_sbindir}/
%{__install} -c -m 644 examples/%{name}.cfg %{buildroot}%{_sysconfdir}/%{name}/
%{__install} -c -m 755 examples/%{name}.init %{buildroot}%{_sysconfdir}/rc.d/init.d/%{name}
%{__install} -c -m 755 doc/%{name}.1 %{buildroot}%{_mandir}/man1/

%{__install} -d -m 0755 %{buildroot}%{_bindir}
%{__install} -p -m 0755 ./contrib/halog/halog %{buildroot}%{_bindir}/halog

for httpfile in $(find ./examples/errorfiles/ -type f) 
do
    %{__install} -p -m 0644 $httpfile %{buildroot}%{haproxy_datadir}
done

# convert all text files to utf8
for textfile in $(find ./ -type f -name '*.txt')
do
    mv $textfile $textfile.old
    iconv --from-code ISO8859-1 --to-code UTF-8 --output $textfile $textfile.old
    rm -f $textfile.old
done
 
%pre
getent group %{haproxy_group} >/dev/null || groupadd \
    -g 188 -r %{haproxy_group}
getent passwd %{haproxy_user} >/dev/null || useradd \
    -u 188 -r -g %{haproxy_group} -d %{haproxy_home} \
    -s /sbin/nologin -c "haproxy" %{haproxy_user}
exit 0

%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}
 
%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then
  /sbin/service %{name} stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" -ge "1" ]; then
  /sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi

%files
## [root@dev-obj-reverse-proxy01 SPECS]# ls ../BUILD/haproxy-1.5.10/
## CHANGELOG  LICENSE  Makefile  README  ROADMAP  SUBVERS  VERDATE  VERSION  contrib  debugfiles.list  debuglinks.list  debugsources.list  doc  ebtree  examples  haproxy  haproxy-systemd-wrapper  include  src  tests

%defattr(-,root,root)
%doc CHANGELOG LICENSE README ROADMAP contrib  examples/*.cfg doc/haproxy-en.txt doc/haproxy-fr.txt doc/architecture.txt doc/configuration.txt
%doc contrib tests haproxy-systemd-wrapper examples doc
%doc %{_mandir}/man1/%{name}.1*

%attr(0755,root,root) %{_bindir}/halog
%attr(0755,root,root) %{_sbindir}/%{name}
%dir %{_sysconfdir}/%{name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.cfg
%attr(0755,root,root) %config %{_sysconfdir}/rc.d/init.d/%{name}

%dir %{haproxy_datadir}/README
%dir %{haproxy_datadir}/400.http
%dir %{haproxy_datadir}/403.http
%dir %{haproxy_datadir}/408.http
%dir %{haproxy_datadir}/500.http
%dir %{haproxy_datadir}/502.http
%dir %{haproxy_datadir}/503.http
%dir %{haproxy_datadir}/504.http
##    /usr/bin/halog
##    /usr/share/haproxy/400.http
##    /usr/share/haproxy/403.http
##    /usr/share/haproxy/408.http
##    /usr/share/haproxy/500.http
##    /usr/share/haproxy/502.http
##    /usr/share/haproxy/503.http
##    /usr/share/haproxy/504.http
##    /usr/share/haproxy/README


%changelog
* Thu Jul 28 2015 Naoto Gohko <naoto-gohko@gmo.jp> 1.5.14-1.g2
- updated to 1.5.14

* Mon Mar 02 2015 Naoto Gohko <naoto-gohko@gmo.jp> 1.5.11-1.g2
- useradd : haproxy 

* Thu Feb 19 2015 Naoto Gohko <naoto-gohko@gmo.jp>
- updated to 1.5.11

* Wed Jun 18 2014 Naoto Gohko <naoto-gohko@gmo.jp>
- updated to 1.5-dev26 

* Fri Mar 28 2014 Naoto Gohko <naoto-gohko@gmo.jp>
- updated to 1.5-dev22 snapshot dev22-ss-20140320

* Mon Feb  3 2014 Willy Tarreau <w@1wt.eu>
- updated to 1.5-dev22

* Tue Dec 17 2013 Willy Tarreau <w@1wt.eu>
- updated to 1.5-dev21

* Mon Dec 16 2013 Willy Tarreau <w@1wt.eu>
- updated to 1.5-dev20

* Mon Jun 17 2013 Willy Tarreau <w@1wt.eu>
- updated to 1.5-dev19

* Wed Apr  3 2013 Willy Tarreau <w@1wt.eu>
- updated to 1.5-dev18

* Fri Dec 28 2012 Willy Tarreau <w@1wt.eu>
- updated to 1.5-dev17

* Mon Dec 24 2012 Willy Tarreau <w@1wt.eu>
- updated to 1.5-dev16

* Wed Dec 12 2012 Willy Tarreau <w@1wt.eu>
- updated to 1.5-dev15

* Mon Nov 26 2012 Willy Tarreau <w@1wt.eu>
- updated to 1.5-dev14

* Thu Nov 22 2012 Willy Tarreau <w@1wt.eu>
- updated to 1.5-dev13

* Mon Sep 10 2012 Willy Tarreau <w@1wt.eu>
- updated to 1.5-dev12

* Mon Jun  4 2012 Willy Tarreau <w@1wt.eu>
- updated to 1.5-dev11

* Mon May 14 2012 Willy Tarreau <w@1wt.eu>
- updated to 1.5-dev10

* Tue May  8 2012 Willy Tarreau <w@1wt.eu>
- updated to 1.5-dev9

* Mon Mar 26 2012 Willy Tarreau <w@1wt.eu>
- updated to 1.5-dev8

* Sat Sep 10 2011 Willy Tarreau <w@1wt.eu>
- updated to 1.5-dev7

* Fri Apr  8 2011 Willy Tarreau <w@1wt.eu>
- updated to 1.5-dev6

* Tue Mar 29 2011 Willy Tarreau <w@1wt.eu>
- updated to 1.5-dev5

* Sun Mar 13 2011 Willy Tarreau <w@1wt.eu>
- updated to 1.5-dev4

* Thu Nov 11 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.5-dev3

* Sat Aug 28 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.5-dev2

* Wed Aug 25 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.5-dev1

* Sun May 23 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.5-dev0

* Sun May 16 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.4.6

* Thu May 13 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.4.5

* Wed Apr  7 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.4.4

* Tue Mar 30 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.4.3

* Wed Mar 17 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.4.2

* Thu Mar  4 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.4.1

* Fri Feb 26 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.4.0

* Tue Feb  2 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.4-rc1

* Mon Jan 25 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.4-dev8

* Mon Jan 25 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.4-dev7

* Fri Jan  8 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.4-dev6

* Sun Jan  3 2010 Willy Tarreau <w@1wt.eu>
- updated to 1.4-dev5

* Mon Oct 12 2009 Willy Tarreau <w@1wt.eu>
- updated to 1.4-dev4

* Thu Sep 24 2009 Willy Tarreau <w@1wt.eu>
- updated to 1.4-dev3

* Sun Aug  9 2009 Willy Tarreau <w@1wt.eu>
- updated to 1.4-dev2

* Wed Jul 29 2009 Willy Tarreau <w@1wt.eu>
- updated to 1.4-dev1

* Tue Jun 09 2009 Willy Tarreau <w@1wt.eu>
- updated to 1.4-dev0

* Sun May 10 2009 Willy Tarreau <w@1wt.eu>
- updated to 1.3.18

* Sun Mar 29 2009 Willy Tarreau <w@1wt.eu>
- updated to 1.3.17

* Sun Mar 22 2009 Willy Tarreau <w@1wt.eu>
- updated to 1.3.16

* Sat Apr 19 2008 Willy Tarreau <w@1wt.eu>
- updated to 1.3.15

* Wed Dec  5 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.14

* Thu Oct 18 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.13

* Sun Jun 17 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.12

* Sun Jun  3 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.11.4

* Mon May 14 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.11.3

* Mon May 14 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.11.2

* Mon May 14 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.11.1

* Mon May 14 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.11

* Thu May 10 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.10.2

* Tue May 09 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.10.1

* Tue May 08 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.10

* Sun Apr 15 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.9

* Tue Apr 03 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.8.2

* Sun Apr 01 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.8.1

* Sun Mar 25 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.8

* Wed Jan 26 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.7

* Wed Jan 22 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.6

* Wed Jan 07 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.5

* Wed Jan 02 2007 Willy Tarreau <w@1wt.eu>
- updated to 1.3.4

* Wed Oct 15 2006 Willy Tarreau <w@1wt.eu>
- updated to 1.3.3

* Wed Sep 03 2006 Willy Tarreau <w@1wt.eu>
- updated to 1.3.2

* Wed Jul 09 2006 Willy Tarreau <w@1wt.eu>
- updated to 1.3.1

* Wed May 21 2006 Willy Tarreau <willy@w.ods.org>
- updated to 1.2.14

* Wed May 01 2006 Willy Tarreau <willy@w.ods.org>
- updated to 1.2.13

* Wed Apr 15 2006 Willy Tarreau <willy@w.ods.org>
- updated to 1.2.12

* Wed Mar 30 2006 Willy Tarreau <willy@w.ods.org>
- updated to 1.2.11.1

* Wed Mar 19 2006 Willy Tarreau <willy@w.ods.org>
- updated to 1.2.10

* Wed Mar 15 2006 Willy Tarreau <willy@w.ods.org>
- updated to 1.2.9

* Sat Jan 22 2005 Willy Tarreau <willy@w.ods.org>
- updated to 1.2.3 (1.1.30)

* Sun Nov 14 2004 Willy Tarreau <w@w.ods.org>
- updated to 1.1.29
- fixed path to config and init files
- statically linked PCRE to increase portability to non-pcre systems

* Sun Jun  6 2004 Willy Tarreau <willy@w.ods.org>
- updated to 1.1.28
- added config check support to the init script

* Tue Oct 28 2003 Simon Matter <simon.matter@invoca.ch>
- updated to 1.1.27
- added pid support to the init script

* Wed Oct 22 2003 Simon Matter <simon.matter@invoca.ch>
- updated to 1.1.26

* Thu Oct 16 2003 Simon Matter <simon.matter@invoca.ch>
- initial build
