%bcond_without snmp
%bcond_without vrrp
%bcond_with profile
%bcond_with debug

## GMO
%define snmp 1

Name: keepalived
Summary: Load balancer and high availability service
##Version: 1.2.13
##Version: 1.2.16
Version: 1.2.17
Release: 4.gmo%{?dist}
License: GPLv2+
URL: http://www.keepalived.org/
Group: System Environment/Daemons

Source0: http://www.keepalived.org/software/keepalived-%{version}.tar.gz
Source1: keepalived.init

Patch0: bz1100028-keepalived-man-snmp.patch

Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(postun): /sbin/service

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if %{with snmp}
BuildRequires: net-snmp-devel
%endif
BuildRequires: openssl-devel
BuildRequires: libnl-devel
BuildRequires: kernel-devel
BuildRequires: popt-devel

%description
Keepalived provides simple and robust facilities for load balancing
and high availability.  The load balancing framework relies on the
well-known and widely used Linux Virtual Server (IPVS) kernel module
providing layer-4 (transport layer) load balancing.  Keepalived
implements a set of checkers to dynamically and adaptively maintain
and manage a load balanced server pool according their health.
Keepalived also implements the Virtual Router Redundancy Protocol
(VRRPv2) to achieve high availability with director failover.

%prep
%setup -q
##%%patch0 -p1

%build
%configure \
    %{?with_debug:--enable-debug} \
    %{?with_profile:--enable-profile} \
    %{!?with_vrrp:--disable-vrrp} \
    %{?with_snmp:--enable-snmp}
%{__make} %{?_smp_mflags} STRIP=/bin/true

%install
%{__rm} -rf %{buildroot}
%{__rm} -rf doc/samples/*.pem
%{__make} install DESTDIR=%{buildroot}
%{__rm} -rf %{buildroot}%{_sysconfdir}/keepalived/samples/
%{__install} -p -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}

%if %{with snmp}
%{__mkdir_p} -p %{buildroot}%{_datadir}/snmp/mibs/
%{__install} -p -m 0644 doc/KEEPALIVED-MIB %{buildroot}%{_datadir}/snmp/mibs/KEEPALIVED-MIB.txt
%endif

%clean
%{__rm} -rf %{buildroot}

%post
/sbin/chkconfig --add keepalived

%preun
if [ "$1" -eq 0 ]; then
    /sbin/service keepalived stop >/dev/null 2>&1
    /sbin/chkconfig --del keepalived
fi

%postun
if [ "$1" -eq 1 ]; then
    /sbin/service keepalived condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%doc AUTHOR ChangeLog CONTRIBUTORS COPYING README TODO VERSION
%doc doc/keepalived.conf.SYNOPSIS doc/NOTE_vrrp_vmac.txt doc/samples/
%dir %{_sysconfdir}/keepalived/
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/keepalived/keepalived.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/keepalived
# %%dir /usr/share/snmp/mibs/
# /usr/share/snmp/mibs/KEEPALIVED-MIB
# /usr/share/snmp/mibs/VRRP-MIB
%{_sysconfdir}/rc.d/init.d/keepalived
%if %{with snmp}
%{_datadir}/snmp/mibs/KEEPALIVED-MIB.txt
%{_datadir}/snmp/mibs/KEEPALIVED-MIB
%{_datadir}/snmp/mibs/VRRP-MIB
%endif
%attr(0755,root,root) %{_bindir}/genhash
%attr(0755,root,root) %{_sbindir}/keepalived
%{_mandir}/man1/genhash.1*
%{_mandir}/man5/keepalived.conf.5*
%{_mandir}/man8/keepalived.8*

%changelog
* Thu Jun 09 2015 Naoto Gohko <naoto-gohko@gmo.jp> - 1.2.17-4.gmo
- Rebase to upstream version 1.2.17

* Thu May 14 2015 Naoto Gohko <naoto-gohko@gmo.jp> - 1.2.16-4.gmo
- Rebase to upstream version 1.2.16

* Wed Aug 07 2014 Ryan O'Hara <rohara@redhat.com> - 1.2.13-4
- Bump release number
  Related: rhbz#1100029, rhbz#1100030

* Thu May 22 2014 Ryan O'Hara <rohara@redhat.com> - 1.2.13-3
- Minor spec file modifications
  Resolves: rhbz#1100029, rhbz#1100030

* Wed May 21 2014 Ryan O'Hara <rohara@redhat.com> - 1.2.13-2
- Add SNMP subsystem option to man page
  Resolves: rhbz#1100028

* Wed May 21 2014 Ryan O'Hara <rohara@redhat.com> - 1.2.13-1
- Rebase to upstream version 1.2.13
  Resolves: rhbz#1052380, rhbz#1077201, rhbz#1007575, rhbz#967641

* Wed Sep 26 2012 Ryan O'Hara <rohara@redhat.com> - 1.2.7-3
- Don't strip binaries at build time.
  Resolves: rhbz#846064

* Fri Sep 21 2012 Ryan O'Hara <rohara@redhat.com> - 1.2.7-2
- Bump release number.
  Resolves: rhbz#846064

* Thu Sep 20 2012 Ryan O'Hara <rohara@redhat.com> - 1.2.7-1
- Initial build.
  Resolves: rhbz#846064
