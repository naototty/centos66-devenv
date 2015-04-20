
%define nginx_home %{_localstatedir}/cache/nginx
##%%define user nginx
%define nginx_user nginx
%define nginx_group nginx

%define orig_pkg_name nginx
%define orig_pkg_version 1.7.10

%define mruby_mod_ver 1.8.8
%define mruby_mod_dir ngx_mruby-%{mruby_mod_ver}

# distribution specific definitions
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)

%define homedir %{_usr}/local/openresty

## lua install dir
##%%define lua_lib_dir %%{_sysconfdir}/nginx/lualib
%define lua_lib_dir /usr/lua/lualib
%define lua_bin_dir /usr/lua/bin

##%%define luajit_dir %%{_sysconfdir}/nginx/luajit
%define luajit_dir /usr/lua/luajit

##%%define luajit_include_dir %%{_sysconfdir}/nginx/luajit/include
%define luajit_include_dir %{luajit_dir}/include

##%%define luajit_lib_dir %%{_sysconfdir}/nginx/luajit/lib
%define luajit_lib_dir %{luajit_dir}/lib

##%%define luajit_share_dir %%{_sysconfdir}/nginx/luajit/share
%define luajit_share_dir %{luajit_dir}/share

##%%define luajit_man_dir %%{_sysconfdir}/nginx/luajit/share/man
%define luajit_man_dir %{luajit_dir}/share/man

%if 0%{?rhel}  == 5
Group: System Environment/Daemons
Requires(pre): shadow-utils
Requires: initscripts >= 8.36
Requires(post): chkconfig
Requires: openssl
Requires:	GeoIP-update
Requires:	GeoIP
Requires:	GeoIP-update6
Requires:	geoip-geolite
BuildRequires: GeoIP-devel
BuildRequires: openssl-devel
%endif

%if 0%{?rhel}  == 6
Group: System Environment/Daemons
Requires(pre): shadow-utils
Requires: initscripts >= 8.36
Requires(post): chkconfig
Requires: openssl >= 1.0.1
Requires:	GeoIP-update
Requires:	GeoIP
Requires:	GeoIP-update6
Requires:	geoip-geolite
BuildRequires: GeoIP-devel
BuildRequires: openssl-devel >= 1.0.1
%define with_spdy 1
%endif

%if 0%{?rhel}  == 7
Group: System Environment/Daemons
Requires(pre): shadow-utils
Requires: systemd
Requires: openssl >= 1.0.1
Requires:	GeoIP-update
Requires:	GeoIP
BuildRequires: GeoIP-devel
BuildRequires: systemd
BuildRequires: openssl-devel >= 1.0.1
Epoch: 1
%define with_spdy 1
%endif


Name:		ngx_openresty
Version:	1.7.10.3.g
## ngx_openresty-1.7.10.2.gmo.tar.gz
Release:	1.3.gmo%{?dist}
Summary:	a fast web app server by extending nginx

Group:		Productivity/Networking/Web/Servers
License:	BSD
URL:		openresty.org
Source0:	http://openresty.org/download/%{name}-%{version}.tar.gz
Source1:	https://github.com/brnt/openresty-rpm-spec/raw/master/nginx.init
Source10001: logrotate
Source10002: nginx.init.orig
Source10003: nginx.sysconf
Source10004: nginx.conf
Source10005: nginx.vh.default.conf
Source10006: nginx.vh.example_ssl.conf
Source10007: nginx.suse.init
Source10008: nginx.service
Source10009: nginx.upgrade.sh
Obsoletes: nginx
Provides:  nginx

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
## BuildRoot:	%%(mktemp -ud %%{_tmppath}/%%{name}-%%{version}-%%{release}-XXXXXX)

BuildRequires:	sed openssl-devel readline-devel
BuildRequires: zlib-devel
BuildRequires: pcre-devel
## GeoIP-devel.x86_64 GeoIP-update.noarch GeoIP-update6.noarch GeoIP.x86_64 geoip-geolite.noarch

Requires:	openssl pcre readline
Requires(pre):	shadow-utils

Provides: webserver

%description
nginx [engine x] OpenResty (aka. ngx_openresty) is a full-fledged web application server by bundling the standard Nginx core, lots of 3rd-party Nginx modules, as well as most of their external dependencies.


%package debug
Summary: debug version of nginx
Group: System Environment/Daemons
Requires: nginx
%description debug
Not stripped version of nginx built with the debugging log support.

%prep
%setup -q


%build

./configure \
        --prefix=%{_sysconfdir}/nginx \
        --sbin-path=%{_sbindir}/nginx \
        --conf-path=%{_sysconfdir}/nginx/nginx.conf \
        --error-log-path=%{_localstatedir}/log/nginx/error.log \
        --http-log-path=%{_localstatedir}/log/nginx/access.log \
        --pid-path=%{_localstatedir}/run/nginx.pid \
        --lock-path=%{_localstatedir}/run/nginx.lock \
        --http-client-body-temp-path=%{_localstatedir}/cache/nginx/client_temp \
        --http-proxy-temp-path=%{_localstatedir}/cache/nginx/proxy_temp \
        --http-fastcgi-temp-path=%{_localstatedir}/cache/nginx/fastcgi_temp \
        --http-uwsgi-temp-path=%{_localstatedir}/cache/nginx/uwsgi_temp \
        --http-scgi-temp-path=%{_localstatedir}/cache/nginx/scgi_temp \
     --with-pcre-jit \
   --with-luajit \
   --with-luajit-xcflags='-DLUA_USE_APICHECK -DLUA_USE_ASSERT -DLUA_ROOT=/usr/lua/luajit -DLUA_DEFAULT_PATH="/usr/lua/lualib/?.lua;/etc/nginx/lualib/?/init.lua" -DLUA_DEFAULT_CPATH="/usr/lua/lualib/?.so"' \
        --user=%{nginx_user} \
        --group=%{nginx_group} \
        --with-http_ssl_module \
        --with-http_realip_module \
    --with-http_geoip_module \
        --with-http_addition_module \
        --with-http_sub_module \
        --with-http_dav_module \
        --with-http_flv_module \
        --with-http_mp4_module \
        --with-http_gunzip_module \
        --with-http_gzip_static_module \
        --with-http_random_index_module \
        --with-http_secure_link_module \
        --with-http_stub_status_module \
        --with-http_auth_request_module \
        --with-mail \
        --with-mail_ssl_module \
        --with-file-aio \
        --with-ipv6 \
        --with-debug \
        %{?with_spdy:--with-http_spdy_module} \
        --with-cc-opt="%{optflags} $(pcre-config --cflags)" \
        $*
   ## --without-http_ngx_mruby_module \
## gmake TARGET_STRIP=@: CCDEBUG=-g Q= XCFLAGS='-DLUA_USE_APICHECK -DLUA_USE_ASSERT' CC=cc PREFIX=/etc/nginx/luajit
pushd %{_builddir}/%{name}-%{version}/bundle/%{mruby_mod_dir}
minirake
popd
## == re-write Makefile START ========================================================
cat %{_builddir}/%{name}-%{version}/Makefile | sed \
  -e 's|LUA_CMODULE_DIR=/etc/nginx/lualib|LUA_CMODULE_DIR=/usr/lua/lualib|g' \
  -e 's|LUA_MODULE_DIR=/etc/nginx/lualib|LUA_MODULE_DIR=/usr/lua/lualib|g' \
  -e 's|PREFIX=/etc/nginx/luajit|PREFIX=/usr/lua/luajit|g' \
  -e "s|XCFLAGS='-DLUA_USE_APICHECK -DLUA_USE_ASSERT'|XCFLAGS='-DLUA_USE_APICHECK -DLUA_USE_ASSERT -DLUA_ROOT=/usr/lua/luajit'|g" \
  -e 's|LUA_LIB_DIR=/etc/nginx/lualib|LUA_LIB_DIR=/usr/lua/lualib|g' \
  -e 's|resty $(DESTDIR)//etc/nginx/bin/|resty $(DESTDIR)/usr/lua/bin/|g' > %{_builddir}/%{name}-%{version}/Makefile.new
mv -vf %{_builddir}/%{name}-%{version}/Makefile %{_builddir}/%{name}-%{version}/Makefile.old
cat %{_builddir}/%{name}-%{version}/Makefile.new  > %{_builddir}/%{name}-%{version}/Makefile

## == re-write Makefile END ========================================================
## LUA_ROOT=/usr/lua/luajit make LUA_ROOT=/usr/lua/luajit %{?_smp_mflags}
make %{?_smp_mflags}
## /root/rpmbuild/BUILD/ngx_openresty-1.7.10.1/build/nginx-1.7.10/objs/nginx
%{__mkdir} -p %{_builddir}/%{name}-%{version}/objs
%{__mv} %{_builddir}/%{name}-%{version}/build/%{orig_pkg_name}-%{orig_pkg_version}/objs/nginx \
        %{_builddir}/%{name}-%{version}/objs/nginx.debug
## %%{__mv} %%{_builddir}/%%{name}-%%{version}/objs/nginx \
##        %%{_builddir}/%%{name}-%%{version}/objs/nginx.debug

./configure \
        --prefix=%{_sysconfdir}/nginx \
        --sbin-path=%{_sbindir}/nginx \
        --conf-path=%{_sysconfdir}/nginx/nginx.conf \
        --error-log-path=%{_localstatedir}/log/nginx/error.log \
        --http-log-path=%{_localstatedir}/log/nginx/access.log \
        --pid-path=%{_localstatedir}/run/nginx.pid \
        --lock-path=%{_localstatedir}/run/nginx.lock \
        --http-client-body-temp-path=%{_localstatedir}/cache/nginx/client_temp \
        --http-proxy-temp-path=%{_localstatedir}/cache/nginx/proxy_temp \
        --http-fastcgi-temp-path=%{_localstatedir}/cache/nginx/fastcgi_temp \
        --http-uwsgi-temp-path=%{_localstatedir}/cache/nginx/uwsgi_temp \
        --http-scgi-temp-path=%{_localstatedir}/cache/nginx/scgi_temp \
     --with-pcre-jit \
   --with-luajit \
   --with-luajit-xcflags='-DLUA_USE_APICHECK -DLUA_USE_ASSERT -DLUA_ROOT=/usr/lua/luajit -DLUA_DEFAULT_PATH="/usr/lua/lualib/?.lua;/etc/nginx/lualib/?/init.lua" -DLUA_DEFAULT_CPATH="/usr/lua/lualib/?.so"' \
        --user=%{nginx_user} \
        --group=%{nginx_group} \
        --with-http_ssl_module \
        --with-http_realip_module \
    --with-http_geoip_module \
        --with-http_addition_module \
        --with-http_sub_module \
        --with-http_dav_module \
        --with-http_flv_module \
        --with-http_mp4_module \
        --with-http_gunzip_module \
        --with-http_gzip_static_module \
        --with-http_random_index_module \
        --with-http_secure_link_module \
        --with-http_stub_status_module \
        --with-http_auth_request_module \
        --with-mail \
        --with-mail_ssl_module \
        --with-file-aio \
        --with-ipv6 \
        %{?with_spdy:--with-http_spdy_module} \
        --with-cc-opt="%{optflags} $(pcre-config --cflags)" \
        $*
   ## --without-http_ngx_mruby_module \
## LUA_ROOT=/usr/lua/luajit make LUA_ROOT=/usr/lua/luajit %{?_smp_mflags}
pushd %{_builddir}/%{name}-%{version}/bundle/%{mruby_mod_dir}
minirake
popd
## == re-write Makefile START ========================================================
cat %{_builddir}/%{name}-%{version}/Makefile | sed \
  -e 's|LUA_CMODULE_DIR=/etc/nginx/lualib|LUA_CMODULE_DIR=/usr/lua/lualib|g' \
  -e 's|LUA_MODULE_DIR=/etc/nginx/lualib|LUA_MODULE_DIR=/usr/lua/lualib|g' \
  -e 's|PREFIX=/etc/nginx/luajit|PREFIX=/usr/lua/luajit|g' \
  -e "s|XCFLAGS='-DLUA_USE_APICHECK -DLUA_USE_ASSERT'|XCFLAGS='-DLUA_USE_APICHECK -DLUA_USE_ASSERT -DLUA_ROOT=/usr/lua/luajit'|g" \
  -e 's|LUA_LIB_DIR=/etc/nginx/lualib|LUA_LIB_DIR=/usr/lua/lualib|g' \
  -e 's|resty $(DESTDIR)//etc/nginx/bin/|resty $(DESTDIR)/usr/lua/bin/|g' > %{_builddir}/%{name}-%{version}/Makefile.new
mv -vf %{_builddir}/%{name}-%{version}/Makefile %{_builddir}/%{name}-%{version}/Makefile.old
cat %{_builddir}/%{name}-%{version}/Makefile.new > %{_builddir}/%{name}-%{version}/Makefile
## == re-write Makefile END ========================================================
make %{?_smp_mflags}


%pre
## getent group %%{user} || groupadd -f -r %%{user}
## getent passwd %%{user} || useradd -M -d %%{homedir} -g %%{user} -s /bin/nologin %%{user}
# Add the "nginx" user
getent group %{nginx_group} >/dev/null || groupadd -r %{nginx_group}
getent passwd %{nginx_user} >/dev/null || \
    useradd -r -g %{nginx_group} -s /sbin/nologin \
    -d %{nginx_home} -c "nginx user"  %{nginx_user}
exit 0


%post
# Register the nginx service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset nginx.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add nginx
%endif
    # print site info
    cat <<BANNER
----------------------------------------------------------------------

Thanks for using nginx!

Please find the official documentation for nginx here:
* http://nginx.org/en/docs/

Commercial subscriptions for nginx are available on:
* http://nginx.com/products/

----------------------------------------------------------------------
BANNER

    # Touch and set permisions on default log files on installation

    if [ -d %{_localstatedir}/log/nginx ]; then
        if [ ! -e %{_localstatedir}/log/nginx/access.log ]; then
            touch %{_localstatedir}/log/nginx/access.log
            %{__chmod} 640 %{_localstatedir}/log/nginx/access.log
            %{__chown} nginx:adm %{_localstatedir}/log/nginx/access.log
        fi

        if [ ! -e %{_localstatedir}/log/nginx/error.log ]; then
            touch %{_localstatedir}/log/nginx/error.log
            %{__chmod} 640 %{_localstatedir}/log/nginx/error.log
            %{__chown} nginx:adm %{_localstatedir}/log/nginx/error.log
        fi
    fi
fi


%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable nginx.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop nginx.service >/dev/null 2>&1 ||:
%else
    /sbin/service nginx stop > /dev/null 2>&1
    /sbin/chkconfig --del nginx
%endif
fi


%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service nginx status  >/dev/null 2>&1 || exit 0
    /sbin/service nginx upgrade >/dev/null 2>&1 || echo \
        "Binary upgrade failed, please check nginx's error.log"
fi



%install
##rm -rf %%{buildroot}
%{__rm} -rf $RPM_BUILD_ROOT
## make install DESTDIR=%{buildroot}
%{__make} DESTDIR=$RPM_BUILD_ROOT install

%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/nginx
if [ -d $RPM_BUILD_ROOT%{_sysconfdir}/nginx/html ]; then
## %%{__mv} $RPM_BUILD_ROOT%%{_sysconfdir}/nginx/html $RPM_BUILD_ROOT%{_datadir}/nginx/
cp -avf %{_builddir}/%{name}-%{version}/build/%{orig_pkg_name}-%{orig_pkg_version}/html $RPM_BUILD_ROOT%{_datadir}/nginx/
else
##%%{__mkdir} -p $RPM_BUILD_ROOT%%{_datadir}/nginx/html
cp -avf %{_builddir}/%{name}-%{version}/build/%{orig_pkg_name}-%{orig_pkg_version}/html $RPM_BUILD_ROOT%{_datadir}/nginx/
fi

%{__rm} -f $RPM_BUILD_ROOT%{_sysconfdir}/nginx/*.default
%{__rm} -f $RPM_BUILD_ROOT%{_sysconfdir}/nginx/fastcgi.conf

%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/run/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/cache/nginx

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/nginx.conf
%{__install} -m 644 -p %{SOURCE10004} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/nginx.conf
%{__install} -m 644 -p %{SOURCE10005} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/default.conf
%{__install} -m 644 -p %{SOURCE10006} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/example_ssl.conf

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
%{__install} -m 644 -p %{SOURCE10003} \
   $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/nginx

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE10008 \
        $RPM_BUILD_ROOT%{_unitdir}/nginx.service
%{__mkdir} -p $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/nginx
%{__install} -m755 %SOURCE10009 \
        $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/nginx/upgrade
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
## mkdir -p %%{buildroot}/etc/init.d
## sed -e 's/%%NGINX_CONF_DIR%%/%%{lua: esc,qty=string.gsub(rpm.expand("%%{homedir}"), "/", "\\/"); print(esc)}\/nginx\/conf/g' \
## 	-e 's/%%NGINX_BIN_DIR%%/%%{lua: esc,qty=string.gsub(rpm.expand("%%{homedir}"), "/", "\\/"); print(esc)}\/nginx\/sbin/g' \
## 	%%{SOURCE1} > %%{buildroot}/etc/init.d/nginx
%{__install} -m755 %{SOURCE10002} \
   $RPM_BUILD_ROOT%{_initrddir}/nginx
%endif

# install log rotation stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%{__install} -m 644 -p %{SOURCE10001} \
   $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/nginx
%{__install} -m644 %{_builddir}/%{name}-%{version}/objs/nginx.debug \
   $RPM_BUILD_ROOT%{_sbindir}/nginx.debug


%clean
%{__rm} -rf $RPM_BUILD_ROOT
## rm -rf %%{buildroot}


%files
%defattr(-,root,root,-)
#%{homedir}/*
%{_sbindir}/nginx

%dir %{_sysconfdir}/nginx
%dir %{_sysconfdir}/nginx/conf.d

%config(noreplace) %{_sysconfdir}/nginx/nginx.conf
%config(noreplace) %{_sysconfdir}/nginx/conf.d/default.conf
%config(noreplace) %{_sysconfdir}/nginx/conf.d/example_ssl.conf
%config(noreplace) %{_sysconfdir}/nginx/mime.types
%config(noreplace) %{_sysconfdir}/nginx/fastcgi_params
%config(noreplace) %{_sysconfdir}/nginx/scgi_params
%config(noreplace) %{_sysconfdir}/nginx/uwsgi_params
%config(noreplace) %{_sysconfdir}/nginx/koi-utf
%config(noreplace) %{_sysconfdir}/nginx/koi-win
%config(noreplace) %{_sysconfdir}/nginx/win-utf

%config(noreplace) %{_sysconfdir}/logrotate.d/nginx
%config(noreplace) %{_sysconfdir}/sysconfig/nginx
%if %{use_systemd}
%{_unitdir}/nginx.service
%dir %{_libexecdir}/initscripts/legacy-actions/nginx
%{_libexecdir}/initscripts/legacy-actions/nginx/*
%else
%{_initrddir}/nginx
%endif

%dir %{_datadir}/nginx
%dir %{_datadir}/nginx/html
%{_datadir}/nginx/html/*

%attr(0755,root,root) %dir %{_localstatedir}/cache/nginx
%attr(0755,root,root) %dir %{_localstatedir}/log/nginx

##%%{_sysconfdir}/nginx/bin/resty
%dir %{luajit_dir}
%dir %{luajit_dir}/bin
%{luajit_dir}/bin/*
%dir %{lua_bin_dir}
%{lua_bin_dir}/resty
%dir %{luajit_include_dir}
%dir %{luajit_include_dir}/luajit-2.1
%{luajit_include_dir}/luajit-2.1/*

%dir %{luajit_lib_dir}
%{luajit_lib_dir}/*

%dir %{luajit_share_dir}
%dir %{luajit_share_dir}/luajit-2.1.0-alpha
%{luajit_share_dir}/luajit-2.1.0-alpha/*

%dir %{luajit_man_dir}
%{luajit_man_dir}/man1/luajit.1

%dir %{lua_lib_dir}
%{lua_lib_dir}/cjson.so
%{lua_lib_dir}/rds/parser.so
%{lua_lib_dir}/redis/parser.so

%dir %{lua_lib_dir}/resty
%{lua_lib_dir}/resty/*

%dir %{_sysconfdir}/nginx/nginx/html
%{_sysconfdir}/nginx/nginx/html/50x.html
%{_sysconfdir}/nginx/nginx/html/index.html


## %%attr(755,root,root) /etc/init.d/nginx
## %%{homedir}/luajit/*
## %%{homedir}/lualib/*
## %%{homedir}/nginx
## %%{homedir}/nginx/html/*
## %%{homedir}/nginx/logs
## %%{homedir}/nginx/sbin
## %%{homedir}/nginx/sbin/nginx
## 
## %%{homedir}/nginx/conf
## %%{homedir}/nginx/conf/fastcgi.conf.default
## %%{homedir}/nginx/conf/fastcgi_params.default
## %%{homedir}/nginx/conf/mime.types.default
## %%{homedir}/nginx/conf/nginx.conf.default
## %%{homedir}/nginx/conf/scgi_params.default
## %%{homedir}/nginx/conf/uwsgi_params.default
## 
## %%config %{homedir}/nginx/conf/fastcgi.conf
## %%config %{homedir}/nginx/conf/fastcgi_params
## %%config %{homedir}/nginx/conf/koi-utf
## %%config %{homedir}/nginx/conf/koi-win
## %%config %{homedir}/nginx/conf/mime.types
## %%config %{homedir}/nginx/conf/nginx.conf
## %%config %{homedir}/nginx/conf/scgi_params
## %%config %{homedir}/nginx/conf/uwsgi_params
## %%config %{homedir}/nginx/conf/win-utf

%files debug
%attr(0755,root,root) %{_sbindir}/nginx.debug


%changelog
* Tue Apr 07 2015 Naoto Gohko <naoto-gohko@gmo.jp> - 1.7.10.3.g-1.3.gmo
- enabled mruby build

* Wed Mar 13 2015 Naoto Gohko <naoto-gohko@gmo.jp> - 1.7.10.1-1.2.gmo
- fix el7 build

* Wed Mar 11 2015 Naoto Gohko <naoto-gohko@gmo.jp> - 1.7.10.1-1.1.gmo
- re-pkgage 1.7.10.1 ngx_openresty


