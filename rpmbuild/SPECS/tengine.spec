Summary: A fast webserver with minimal memory-footprint (tengine)
Name: tengine
## Version: 2.0.0
Version: 2.1.0
Release: 1.1.gmo%{dist}
Source0: %{name}-%version.tar.gz
Source1: nginx.demo
Source2: nginx.conf.demo
Source3: fcgi.conf.demo
Source4: tengine.service
Source5: tengine.logrotate
Packager: haulm@126.com
License: GPL
Group: Networking/Daemons
URL: http://tengine.taobao.org/
#URL: http://sysoev.ru/nginx/download.html
Requires: pcre zlib php
BuildPrereq: libtool zlib-devel
BuildRoot: %{_tmppath}/%{name}-root

%description
nginx is intented to be a frontend for ad-servers which have to deliver
small files concurrently to many connections.
Tengine is a web server developed by the Servers Platform Team at Taobao.
It is based on the popular Nginx HTTP server with many convenient features.
Tengine has been proven stable and efficient on very busy websites, 
e.g. taobao.com and tmall.com.
We're pleased to announce that Tengine now becomes an open source project.


%prep

%setup -q -n %{name}-%{version}
%build
rm -rf %{buildroot}
./configure --prefix=/usr \
--conf-path=/etc/%{name}/%{name}.conf \
--http-log-path=/var/log/%{name}/%{name}-access.log \
--error-log-path=/var/log/%{name}/%{name}-error.log \
--pid-path=/var/run/%{name}/%{name}.pid \
--with-http_ssl_module \
--with-http_stub_status_module \
--with-http_geoip_module
#--with-http_stub_status_module (安装可以查看nginx状态的程序)
#--with-http_memcached_module (启用memcache缓存)
#--with-http_rewrite_module (启用支持url重写)

## [root@dev-iso-upload01 tengine-2.1.0]# ./configure --help
## 
##   --help                             print this message
## 
##   --prefix=PATH                      set installation prefix
##   --sbin-path=PATH                   set nginx binary pathname
##   --conf-path=PATH                   set nginx.conf pathname
##   --error-log-path=PATH              set error log pathname
##   --pid-path=PATH                    set nginx.pid pathname
##   --lock-path=PATH                   set nginx.lock pathname
## 
##   --user=USER                        set non-privileged user for
##                                      worker processes
##   --group=GROUP                      set non-privileged group for
##                                      worker processes
## 
##   --builddir=DIR                     set build directory
## 
##   --enable-mods-shared=all           enable all the modules to be shared
##   --enable-mods-static=all           enable all the modules to be static
## 
##   --dso-path=DIR                     set dso default load path
##   --dso-tool-path=DIR                set dso_tool pathname
##   --dso-max-modules=*)               set max dso module(default is 256)
##   --includedir=DIR                   set C header files[PREFIX/include]
## 
##   --with-rtsig_module                enable rtsig module
##   --with-select_module               enable select module
##   --without-select_module            disable select module
##   --with-poll_module                 enable poll module
##   --without-poll_module              disable poll module
## 
##   --without-procs                    disable procs module
## 
##   --with-file-aio                    enable file AIO support
##   --with-ipv6                        enable IPv6 support
## 
##   --without-syslog                   disable syslog logging
## 
##   --without-dso                      disable dso module load
## 
##   --with-http_spdy_module            enable ngx_http_spdy_module
##   --with-http_realip_module          enable ngx_http_realip_module
##   --with-http_addition_module        enable ngx_http_addition_filter_module
##   --with-http_xslt_module            enable ngx_http_xslt_filter_module
##   --with-http_image_filter_module    enable ngx_http_image_filter_module
##   --with-http_geoip_module           enable ngx_http_geoip_module
##   --with-http_sub_module             enable ngx_http_sub_filter_module
##   --with-http_dav_module             enable ngx_http_dav_module
##   --with-http_flv_module             enable ngx_http_flv_module
##   --with-http_slice_module           enable ngx_http_slice_module
##   --with-http_mp4_module             enable ngx_http_mp4_module
##   --with-http_gunzip_module          enable ngx_http_gunzip_module
##   --with-http_gzip_static_module     enable ngx_http_gzip_static_module
##   --with-http_auth_request_module    enable ngx_http_auth_request_module
##   --with-http_concat_module          enable ngx_http_concat_module
##   --with-http_random_index_module    enable ngx_http_random_index_module
##   --with-http_secure_link_module     enable ngx_http_secure_link_module
##   --with-http_degradation_module     enable ngx_http_degradation_module
##   --with-http_sysguard_module        enable ngx_http_sysguard_module
## 
##   --with-http_addition_module=shared enable ngx_http_addition_filter_module (shared)
##   --with-http_xslt_module=shared     enable ngx_http_xslt_filter_module (shared)
##   --with-http_image_filter_module=shared
##                                      enable ngx_http_image_filter_module (shared)
##   --with-http_geoip_module=shared    enable ngx_http_geoip_module
##   --with-http_sub_module=shared      enable ngx_http_sub_filter_module (shared)
##   --with-http_flv_module=shared      enable ngx_http_flv_module (shared)
##   --with-http_slice_module=shared    enable ngx_http_slice_module (shared)
##   --with-http_mp4_module=shared      enable ngx_http_mp4_module (shared)
##   --with-http_concat_module=shared   enable ngx_http_concat_module (shared)
##   --with-http_random_index_module=shared
##                                      enable ngx_http_random_index_module (shared)
##   --with-http_secure_link_module=shared
##                                      enable ngx_http_secure_link_module (shared)
##   --with-http_sysguard_module=shared enable ngx_http_sysguard_module (shared)
##   --with-http_charset_filter_module=shared
##                                      enable ngx_http_charset_filter_module (shared)
##   --with-http_userid_filter_module=shared
##                                      enable ngx_http_userid_filter_module (shared)
##   --with-http_footer_filter_module=shared
##                                      enable ngx_http_footer_filter_module (shared)
##   --with-http_trim_filter_module=shared
##                                      enable ngx_http_trim_filter_module (shared)
##   --with-http_access_module=shared   enable ngx_http_access_module (shared)
##   --with-http_autoindex_module=shared
##                                      enable ngx_http_autoindex_module (shared)
##   --with-http_map_module=shared      enable ngx_http_map_module (shared)
##   --with-http_split_clients_module=shared
##                                      enable ngx_http_split_clients_module (shared)
##   --with-http_referer_module=shared  enable ngx_http_referer_module (shared)
##   --with-http_rewrite_module=shared  enable ngx_http_rewrite_module (shared)
##   --with-http_fastcgi_module=shared  enable ngx_http_fastcgi_module (shared)
##   --with-http_uwsgi_module=shared    enable ngx_http_uwsgi_module (shared)
##   --with-http_scgi_module=shared     enable ngx_http_scgi_module (shared)
##   --with-http_memcached_module=shared
##                                      enable ngx_http_memcached_module (shared)
##   --with-http_limit_conn_module=shared
##                                      enable ngx_http_limit_conn_module (shared)
##   --with-http_limit_req_module=shared
##                                      enable ngx_http_limit_req_module (shared)
##   --with-http_empty_gif_module=shared
##                                      enable ngx_http_empty_gif_module (shared)
##   --with-http_browser_module=shared  enable ngx_http_browser_module (shared)
##   --with-http_user_agent_module=shared
##                                      enable ngx_http_user_agent_module (shared)
##   --with-http_upstream_ip_hash_module=shared
##                                      enable ngx_http_upstream_ip_hash_module (shared)
##   --with-http_upstream_least_conn_module=shared
##                                      enable ngx_http_upstream_least_conn_module (shared)
##   --with-http_upstream_session_sticky_module=shared
##                                      enable ngx_http_upstream_session_sticky_module (shared)
##   --with-http_reqstat_module=shared  enable ngx_http_reqstat_module (shared)
## 
##   --without-http_charset_module      disable ngx_http_charset_filter_module
##   --without-http_gzip_module         disable ngx_http_gzip_filter_module
##   --without-http_ssi_module          disable ngx_http_ssi_module
##   --without-http_ssl_module          disable ngx_http_ssl_module
##   --without-http_userid_module       disable ngx_http_userid_filter_module
##   --without-http_footer_filter_module
##                                      disable ngx_http_footer_filter_module
##   --without-http_trim_filter_module  disable ngx_http_trim_filter_module
##   --without-http_access_module       disable ngx_http_access_module
##   --without-http_auth_basic_module   disable ngx_http_auth_basic_module
##   --without-http_autoindex_module    disable ngx_http_autoindex_module
##   --without-http_geo_module          disable ngx_http_geo_module
##   --without-http_map_module          disable ngx_http_map_module
##   --without-http_split_clients_module
##                                      disable ngx_http_split_clients_module
##   --without-http_referer_module      disable ngx_http_referer_module
##   --without-http_rewrite_module      disable ngx_http_rewrite_module
##   --without-http_proxy_module        disable ngx_http_proxy_module
##   --without-http_fastcgi_module      disable ngx_http_fastcgi_module
##   --without-http_uwsgi_module        disable ngx_http_uwsgi_module
##   --without-http_scgi_module         disable ngx_http_scgi_module
##   --without-http_memcached_module    disable ngx_http_memcached_module
##   --without-http_limit_conn_module   disable ngx_http_limit_conn_module
##   --without-http_limit_req_module    disable ngx_http_limit_req_module
##   --without-http_empty_gif_module    disable ngx_http_empty_gif_module
##   --without-http_browser_module      disable ngx_http_browser_module
##   --without-http_upstream_check_module
##                                      disable ngx_http_upstream_check_module
##   --without-http_upstream_least_conn_module
##                                      disable ngx_http_upstream_least_conn_module
##   --without-http_upstream_session_sticky_module
##                                      disable ngx_http_upstream_session_sticky_module
##   --without-http_upstream_keepalive_module
##                                      disable ngx_http_upstream_keepalive_module
##   --without-http_upstream_dynamic_module
##                                      disable ngx_http_upstream_dynamic_module
##   --without-http_upstream_ip_hash_module
##                                      disable ngx_http_upstream_ip_hash_module
##   --without-http_upstream_consistent_hash_module
##                                      disable ngx_http_upstream_consistent_hash_module
##   --without-http_user_agent_module   disable ngx_http_user_agent_module
##   --without-http_stub_status_module  disable ngx_http_stub_status_module
##   --without-http_reqstat_module      disable ngx_http_reqstat_module
## 
##   --with-http_perl_module            enable ngx_http_perl_module
##   --with-perl_modules_path=PATH      set Perl modules path
##   --with-perl=PATH                   set perl binary pathname
## 
##   --without-http-upstream-rbtree     disable using rbtree for upstream lookup
## 
##   --with-http_lua_module             enable ngx_http_lua_module (will also enable --with-md5 and --with-sha1)
##   --with-http_lua_module=shared      enable ngx_http_lua_module (shared) (will also enable --with-md5 and --with-sha1)
##   --with-luajit-inc=PATH             set LuaJIT headers path (where lua.h/lauxlib.h/... are located)
##   --with-luajit-lib=PATH             set LuaJIT library path (where libluajit-5.1.{a,so} are located)
##   --with-lua-inc=PATH                set Lua headers path (where lua.h/lauxlib.h/... are located)
##   --with-lua-lib=PATH                set Lua library path (where liblua.{a,so} are located, only support Lua-5.1.x)
## 
##   --with-http_tfs_module             enable ngx_http_tfs_module (will also enable --with-md5)
##   --with-http_tfs_module=shared      enable ngx_http_tfs_module (shared) (will also enable --with-md5)
##   --with-libyajl-inc=PATH            set libyajl headers path (where yajl.h is located)
##   --with-libyajl-lib=PATH            set libyajl library path (where libyajl.{a,so} is located)
## 
##   --http-log-path=PATH               set http access log pathname
##   --http-client-body-temp-path=PATH  set path to store
##                                      http client request body temporary files
##   --http-proxy-temp-path=PATH        set path to store
##                                      http proxy temporary files
##   --http-fastcgi-temp-path=PATH      set path to store
##                                      http fastcgi temporary files
##   --http-uwsgi-temp-path=PATH        set path to store
##                                      http uwsgi temporary files
##   --http-scgi-temp-path=PATH         set path to store
##                                      http scgi temporary files
## 
##   --without-http                     disable HTTP server
##   --without-http-cache               disable HTTP cache
## 
##   --with-mail                        enable POP3/IMAP4/SMTP proxy module
##   --with-mail_ssl_module             enable ngx_mail_ssl_module
##   --without-mail_pop3_module         disable ngx_mail_pop3_module
##   --without-mail_imap_module         disable ngx_mail_imap_module
##   --without-mail_smtp_module         disable ngx_mail_smtp_module
## 
##   --with-google_perftools_module     enable ngx_google_perftools_module
##   --with-cpp_test_module             enable ngx_cpp_test_module
##   --with-backtrace_module            enable ngx_backtrace_module
## 
##   --add-module=PATH                  enable an external module
## 
##   --with-cc=PATH                     set C compiler pathname
##   --with-cpp=PATH                    set C preprocessor pathname
##   --with-cc-opt=OPTIONS              set additional C compiler options
##   --with-ld-opt=OPTIONS              set additional linker options
##   --with-cpu-opt=CPU                 build for the specified CPU, valid values:
##                                      pentium, pentiumpro, pentium3, pentium4,
##                                      athlon, opteron, sparc32, sparc64, ppc64
## 
##   --without-pcre                     disable PCRE library usage
##   --with-pcre                        force PCRE library usage
##   --with-pcre=DIR                    set path to PCRE library sources
##   --with-pcre-opt=OPTIONS            set additional build options for PCRE
##   --with-pcre-jit                    build PCRE with JIT compilation support
## 
##   --with-md5=DIR                     set path to md5 library sources
##   --with-md5-opt=OPTIONS             set additional build options for md5
##   --with-md5-asm                     use md5 assembler sources
## 
##   --with-sha1=DIR                    set path to sha1 library sources
##   --with-sha1-opt=OPTIONS            set additional build options for sha1
##   --with-sha1-asm                    use sha1 assembler sources
## 
##   --with-zlib=DIR                    set path to zlib library sources
##   --with-zlib-opt=OPTIONS            set additional build options for zlib
##   --with-zlib-asm=CPU                use zlib assembler sources optimized
##                                      for the specified CPU, valid values:
##                                      pentium, pentiumpro
## 
##   --with-libatomic                   force libatomic_ops library usage
##   --with-libatomic=DIR               set path to libatomic_ops library sources
## 
##   --with-jemalloc                    force jemalloc library usage
##   --with-jemalloc=DIR                set path to jemalloc library files
## 
##   --with-openssl=DIR                 set path to OpenSSL library sources
##   --with-openssl-opt=OPTIONS         set additional build options for OpenSSL
## 
##   --with-debug                       enable debug logging
## 
## [root@dev-iso-upload01 tengine-2.1.0]#


make
%install
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/init.d/
#mkdir -p %{buildroot}/usr/lib/systemd/system/
mkdir -p %{buildroot}/var/log/%{name}
mkdir -p %{buildroot}/etc
mkdir -p %{buildroot}/etc/logrotate.d/
rm -rf %{buildroot}/etc/nginx.conf
#install -m 777 %{SOURCE1} %{buildroot}%{_sysconfdir}/init.d/tengine
install -m 777 %{SOURCE1} %{buildroot}%{_sysconfdir}/init.d/tengine
install -m 644 %{SOURCE2} %{buildroot}/etc/tengine.conf
install -m 644 %{SOURCE3} %{buildroot}/etc/fcgi.conf
##install -m 644 %{SOURCE4} %{buildroot}/usr/lib/systemd/system/tengine.service
install -m 644 %{SOURCE5} %{buildroot}/etc/logrotate.d/tengine
%clean
rm -rf %{buildroot}
%post
useradd www
%files
%defattr(-,root,root)
/etc/%{name}/browsers
/etc/logrotate.d/tengine
/usr/sbin/nginx
/etc/%{name}/fastcgi.conf
/etc/%{name}/fastcgi.conf.default
/etc/%{name}/fastcgi_params
/etc/%{name}/fastcgi_params.default
/etc/%{name}/fcgi.conf
/etc/init.d/tengine
##/usr/lib/systemd/system/tengine.service
/etc/%{name}/koi-utf
/etc/%{name}/koi-win
/etc/%{name}/mime.types
/etc/%{name}/mime.types.default
/etc/%{name}/nginx.conf.default
/etc/%{name}/scgi_params
/etc/%{name}/scgi_params.default
/etc/%{name}/tengine.conf
/etc/%{name}/uwsgi_params
/etc/%{name}/uwsgi_params.default
/etc/%{name}/win-utf
/etc/%{name}/module_stubs
/usr/sbin/dso_tool
/usr/include/nginx.h
/usr/include/*
%exclude /usr/html
%changelog

