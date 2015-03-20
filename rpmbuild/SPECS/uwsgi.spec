%define perl_ver  %(eval "`%{__perl} -V:version`"; echo $version)
%define php_apiv  %((echo 0; php -i 2>/dev/null | grep "PHP API" | tr -d '[:alpha:][:punct:][:blank:]') | tail -1)
%define python_abi %(%{__python} -c "import sys; print sys.version[:3]")
%define ruby_abi  %(ruby -rrbconfig -e "puts Config::CONFIG['ruby_version']" 2>/dev/null || echo 'None')
%define lua_abi   %(pkg-config lua --variable="V" 2>/dev/null || echo 'None')
%define httpd_mmn %(%{__cat} %{_includedir}/httpd/.mmn 2>/dev/null || echo '0-0')


Summary:          A fast, self-healing, application container server
Name:             uwsgi
Version:          2.0.3
Release:          1%{?dist}%{?pext}
License:          GPLv2
Group:            System Environment/Daemons
Source0:          http://projects.unbit.it/downloads/%{name}-%{version}.tar.gz
Source1:          %{name}.init
Source2:          %{name}.sysconfig
Source3:          %{name}.logrotate
Source4:          %{name}.conf
Patch0:           %{name}-2.0.1-build.patch
Patch1:           %{name}-2.0.1-java.patch
URL:              http://projects.unbit.it/%{name}/
Buildroot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Vendor:           The uWSGI project
Requires(pre):    /usr/sbin/groupadd /usr/sbin/useradd
Requires(post):   /sbin/chkconfig
Requires(preun):  /sbin/chkconfig /sbin/service
Requires(postun): /sbin/service
BuildRequires:    libattr-devel libcap-devel libuuid-devel
BuildRequires:    libxml2-devel openssl-devel pcre-devel
BuildRequires:    zlib-devel

%description
uWSGI is a fast, self-healing, application container server. Born as
a WSGI-only server, over time it has evolved in a complete stack for
networked/clustered web applications. It uses the uwsgi protocol for
all the networking/interprocess communications, but can speak other
protocols as well. uWSGI is designed to be fully modular, which means
that different plugins can be used in order to add compatibility with
tons of different technology on top of the same core.


%package          curl
Summary:          Curl plugin for uWSGI
Group:            System Environment/Libraries
Requires:         %{name} = %{version}-%{release}
BuildRequires:    curl-devel

%description      curl
The %{name}-curl package provides the Curl plugin for uWSGI.


%package          java
Summary:          Java language support for uWSGI
Group:            System Environment/Libraries
Requires:         %{name} = %{version}-%{release}
Requires:         jre7-openjdk java7 = 1:1.7.0
BuildRequires:    java-1.7.0-openjdk-devel

%description      java
The %{name}-java package provides Java language support for uWSGI.


%package          ldap
Summary:          LDAP support for uWSGI
Group:            System Environment/Libraries
Requires:         %{name} = %{version}-%{release}
BuildRequires:    openldap-devel

%description      ldap
The %{name}-ldap package provides LDAP support for uWSGI.


%package          lua
Summary:          Lua language support for uWSGI
Group:            System Environment/Libraries
Requires:         %{name} = %{version}-%{release}
Requires:         lua(abi) = %{lua_abi}
BuildRequires:    lua52-devel

%description      lua
The %{name}-lua package provides Lua language support for uWSGI.


%package          perl
Summary:          Perl language support for uWSGI
Group:            System Environment/Libraries
Requires:         %{name} = %{version}-%{release}
Requires:         perl(:MODULE_COMPAT_%{perl_ver})
BuildRequires:    perl-devel perl-ExtUtils-Embed

%description      perl
The %{name}-perl package provides Perl language support for uWSGI.


%package          php
Summary:          PHP language support for uWSGI
Group:            System Environment/Libraries
Requires:         %{name} = %{version}-%{release}
Requires:         php-api = %{php_apiv}
BuildRequires:    bzip2-devel gmp-devel libedit-devel
BuildRequires:    openssl-devel php-devel php-embedded

%description      php
The %{name}-php package provides PHP language support for uWSGI.


%package          python
Summary:          Python language support for uWSGI
Group:            System Environment/Libraries
Requires:         %{name} = %{version}-%{release}
Requires:         python(abi) = %{python_abi}
BuildRequires:    python-devel

%description      python
The %{name}-python package provides Python language support for uWSGI.


%package          rrdtool
Summary:          RRDtool plugin for uWSGI
Group:            System Environment/Libraries
Requires:         %{name} = %{version}-%{release}

%description      rrdtool
The %{name}-rrdtool package provides the RRDtool plugin for uWSGI.


%package          ruby
Summary:          Ruby language support for uWSGI
Group:            System Environment/Libraries
Requires:         %{name} = %{version}-%{release}
Requires:         ruby(abi) = %{ruby_abi}
BuildRequires:    ruby ruby-devel

%description      ruby
The %{name}-ruby package provides Ruby language support for uWSGI.


%package          xslt
Summary:          XSLT support for uWSGI
Group:            System Environment/Libraries
Requires:         %{name} = %{version}-%{release}
BuildRequires:    libxslt-devel

%description      xslt
The %{name}-xslt package provides XSLT support for uWSGI.


%package       -n mod_%{name}
Summary:          uWSGI modules for the Apache HTTP server
Group:            System Environment/Libraries
Provides:         httpd-mod(%{name}) = %{version}-%{release}
Provides:         httpd-mod(proxy_%{name}) = %{version}-%{release}
Requires:         httpd-mmn = %{httpd_mmn}
BuildRequires:    httpd-devel

%description   -n mod_%{name}
The mod_%{name} package provides the native (deprecated) as well as
the mod_proxy uWSGI plugin for the Apache HTTP server.


%prep
%setup -q
%patch0 -p1
%patch1 -p1

# Create build config
%{__cat} << \_EOF_ >buildconf/rpm.ini
[uwsgi]
main_plugin =
inherit = base
embedded_plugins = null
plugin_dir = %{_libdir}/%{name}
_EOF_


%build
export UWSGICONFIG_LUAPC="lua"

# Build core
%{__python} uwsgiconfig.py --build rpm -g

# Build base plugins
for PLUGIN in \
	ping cache nagios rrdtool carbon rpc corerouter fastrouter http     \
	ugreen signal syslog rsyslog logsocket router_uwsgi router_redirect \
	router_basicauth zergpool redislog mongodblog router_rewrite        \
	router_http logfile router_cache rawrouter router_static sslrouter  \
	spooler cheaper_busyness symcall transformation_tofile              \
	transformation_gzip transformation_chunked transformation_offload   \
	router_memcached router_redis router_hash router_expires            \
	router_metrics transformation_template stats_pusher_socket; do
  %{__python} uwsgiconfig.py --plugin plugins/${PLUGIN} rpm -g
done

# Build extra plugins (excluded: coroae gccgo mongrel2 mono rados tuntap v8)
for PLUGIN in \
	python gevent psgi lua rack jvm jwsgi ring transformation_toupper   \
	php cgi xslt webdav ssi ldap pypy zabbix curl_cron tornado pty      \
	alarm_curl airbrake router_radius; do
  %{__python} uwsgiconfig.py --plugin plugins/${PLUGIN} rpm -g
done

# Build Apache modules
pushd apache2
%{_sbindir}/apxs -c mod_uwsgi.c
%{_sbindir}/apxs -c mod_proxy_uwsgi.c
popd


%install
[ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != "/" ] && %{__rm} -rf ${RPM_BUILD_ROOT}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_initrddir}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_sysconfdir}/{httpd/conf.d,logrotate.d,sysconfig}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_bindir}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_libdir}/{httpd/modules,%{name}}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_javadir}

%{__install} -m 0755 %{name}     ${RPM_BUILD_ROOT}%{_bindir}
%{__install} -m 0755 *_plugin.so ${RPM_BUILD_ROOT}%{_libdir}/%{name}

pushd plugins/jvm
%{__install} -m 0644 %{name}.jar ${RPM_BUILD_ROOT}%{_javadir}
popd

%{__install} -m 0755 %{SOURCE1}  ${RPM_BUILD_ROOT}%{_initrddir}/%{name}
%{__install} -m 0644 %{SOURCE2}  ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/%{name}
%{__install} -m 0644 %{SOURCE3}  ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/%{name}
%{__install} -m 0644 %{SOURCE4}  ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf.d

# Install Apache modules
pushd apache2
%{__install} -m 0755 .libs/*.so  ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules
popd


%pre
if ! getent group  %{name} >/dev/null 2>&1; then
  /usr/sbin/groupadd -r %{name}
fi
if ! getent passwd %{name} >/dev/null 2>&1; then
  /usr/sbin/useradd  -r -g %{name}   \
	-d / -c "uWSGI Service user" \
	-M -s /sbin/nologin %{name}
fi
exit 0			# Always pass


%post
/sbin/chkconfig --add %{name}


%preun
if [ $1 -eq 0 ]; then	# Remove
  /sbin/service %{name} stop >/dev/null 2>&1
  /sbin/chkconfig --del %{name}
fi


%postun
if [ $1 -ge 1 ]; then	# Upgrade
  /sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi

%postun -n mod_%{name}
# Restart after erase/upgrade
/sbin/service httpd condrestart >/dev/null 2>&1 || :


%clean
[ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != "/" ] && %{__rm} -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc CONTRIBUTORS LICENSE README *.png
%doc %dir examples
%{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_bindir}/%{name}
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/cache_plugin.so
%{_libdir}/%{name}/carbon_plugin.so
%{_libdir}/%{name}/cgi_plugin.so
%{_libdir}/%{name}/cheaper_busyness_plugin.so
%{_libdir}/%{name}/corerouter_plugin.so
%{_libdir}/%{name}/fastrouter_plugin.so
%{_libdir}/%{name}/http_plugin.so
%{_libdir}/%{name}/logfile_plugin.so
%{_libdir}/%{name}/logsocket_plugin.so
%{_libdir}/%{name}/mongodblog_plugin.so
%{_libdir}/%{name}/nagios_plugin.so
%{_libdir}/%{name}/ping_plugin.so
%{_libdir}/%{name}/pty_plugin.so
%{_libdir}/%{name}/rawrouter_plugin.so
%{_libdir}/%{name}/redislog_plugin.so
%{_libdir}/%{name}/router_basicauth_plugin.so
%{_libdir}/%{name}/router_cache_plugin.so
%{_libdir}/%{name}/router_expires_plugin.so
%{_libdir}/%{name}/router_hash_plugin.so
%{_libdir}/%{name}/router_http_plugin.so
%{_libdir}/%{name}/router_memcached_plugin.so
%{_libdir}/%{name}/router_metrics_plugin.so
%{_libdir}/%{name}/router_radius_plugin.so
%{_libdir}/%{name}/router_redirect_plugin.so
%{_libdir}/%{name}/router_redis_plugin.so
%{_libdir}/%{name}/router_rewrite_plugin.so
%{_libdir}/%{name}/router_static_plugin.so
%{_libdir}/%{name}/router_uwsgi_plugin.so
%{_libdir}/%{name}/rpc_plugin.so
%{_libdir}/%{name}/rsyslog_plugin.so
%{_libdir}/%{name}/signal_plugin.so
%{_libdir}/%{name}/spooler_plugin.so
%{_libdir}/%{name}/ssi_plugin.so
%{_libdir}/%{name}/sslrouter_plugin.so
%{_libdir}/%{name}/stats_pusher_socket_plugin.so
%{_libdir}/%{name}/symcall_plugin.so
%{_libdir}/%{name}/syslog_plugin.so
%{_libdir}/%{name}/transformation_chunked_plugin.so
%{_libdir}/%{name}/transformation_gzip_plugin.so
%{_libdir}/%{name}/transformation_offload_plugin.so
%{_libdir}/%{name}/transformation_template_plugin.so
%{_libdir}/%{name}/transformation_tofile_plugin.so
%{_libdir}/%{name}/transformation_toupper_plugin.so
%{_libdir}/%{name}/ugreen_plugin.so
%{_libdir}/%{name}/webdav_plugin.so
%{_libdir}/%{name}/zabbix_plugin.so
%{_libdir}/%{name}/zergpool_plugin.so

%files curl
%defattr(-,root,root)
%{_libdir}/%{name}/airbrake_plugin.so
%{_libdir}/%{name}/alarm_curl_plugin.so
%{_libdir}/%{name}/curl_cron_plugin.so

%files java
%defattr(-,root,root)
%{_libdir}/%{name}/jvm_plugin.so
%{_libdir}/%{name}/jwsgi_plugin.so
%{_libdir}/%{name}/ring_plugin.so
%{_javadir}/%{name}.jar

%files ldap
%defattr(-,root,root)
%{_libdir}/%{name}/ldap_plugin.so

%files lua
%defattr(-,root,root)
%{_libdir}/%{name}/lua_plugin.so

%files perl
%defattr(-,root,root)
%{_libdir}/%{name}/psgi_plugin.so

%files php
%defattr(-,root,root)
%{_libdir}/%{name}/php_plugin.so

%files python
%defattr(-,root,root)
%{_libdir}/%{name}/gevent_plugin.so
%{_libdir}/%{name}/pypy_plugin.so
%{_libdir}/%{name}/python_plugin.so
%{_libdir}/%{name}/tornado_plugin.so

%files rrdtool
%defattr(-,root,root)
%{_libdir}/%{name}/rrdtool_plugin.so

%files ruby
%defattr(-,root,root)
%{_libdir}/%{name}/rack_plugin.so

%files xslt
%defattr(-,root,root)
%{_libdir}/%{name}/xslt_plugin.so

%files -n mod_%{name}
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%{_libdir}/httpd/modules/mod_uwsgi.so
%{_libdir}/httpd/modules/mod_proxy_uwsgi.so


%changelog
* Wed Mar 19 2014 Peter Pramberger <peterpramb@member.fsf.org> - 2.0.3-1
- New version (2.0.3)

* Sat Mar 01 2014 Peter Pramberger <peterpramb@member.fsf.org> - 2.0.2-1
- New version (2.0.2)

* Mon Feb 24 2014 Peter Pramberger <peterpramb@member.fsf.org> - 2.0.1-1
- Initial build
