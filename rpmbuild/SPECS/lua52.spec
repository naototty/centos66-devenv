%define pkg       lua
%define ver       5.2.3
%define maj       %(echo %{ver} | cut -d'.' -f1)
%define min       %(echo %{ver} | cut -d'.' -f2)
%define pkg_str   %{pkg}%{maj}%{min}
%define abi_ver   %{maj}.%{min}


Summary:          A powerful embeddable scripting language
Name:             %{pkg_str}
Version:          %{ver}
Release:          1%{?dist}%{?pext}
License:          MIT/X11
Group:            Development/Languages
Source0:          http://www.%{pkg}.org/ftp/%{pkg}-%{ver}.tar.gz
Patch0:           %{pkg}-5.2.0-paths.patch
Patch1:           %{pkg}-5.2.1-dynamic.patch
Patch2:           %{pkg}-5.2.3-readline.patch
URL:              http://www.%{pkg}.org/
Buildroot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Vendor:           The Lua Team <team@lua.org>
Requires:         %{name}-lib = %{version}-%{release}
BuildRequires:    ncurses-devel readline-devel

%description
Lua is a powerful, fast, light-weight, embeddable scripting language. It
combines simple procedural syntax with powerful data description constructs
based on associative arrays and extensible semantics. Lua is dynamically
typed, runs by interpreting bytecode for a register-based virtual machine,
and has automatic memory management with incremental garbage collection,
making it ideal for configuration, scripting, and rapid prototyping.


%package          devel
Summary:          Development tools for Lua
Group:            Development/Libraries
Requires:         %{name}-lib = %{version}-%{release}
Requires:         pkgconfig
Conflicts:        %{pkg}-devel < %{version}-%{release}

%description      devel
The %{name}-devel package contains the libraries and header files for
developing software using Lua.


%package          lib
Summary:          The Lua interpreter library
Group:            System Environment/Libraries
Provides:         %{pkg}(abi) = %{abi_ver}

%description      lib
The %{name}-lib package contains the Lua interpreter as shared library.


%package          static
Summary:          Static libraries for Lua
Group:            Development/Libraries
Requires:         %{name}-devel = %{version}-%{release}
Conflicts:        %{pkg}-devel < %{version}-%{release}
Conflicts:        %{pkg}-static < %{version}-%{release}

%description      static
The %{name}-static package contains the statically linkable libraries for
Lua.


%prep
%setup -q -n %{pkg}-%{ver}
%patch0 -p1
%patch1 -p1
%patch2 -p1

# Fix config
for FILE in Makefile etc/lua.pc src/luaconf.h; do
  %{__sed} -i -e 's#XXX_PREFIX_XXX#%{_prefix}#g' \
	      -e 's#XXX_VER_XXX#%{maj}.%{min}#g' \
	      -e 's#XXX_REL_XXX#%{ver}#g'        \
	      -e 's#/lib#/%{_lib}#g'             \
	      -e 's#lib/lua#%{_lib}/lua#g'       \
	      -e 's#/man/#/share/man/#g' ${FILE}
done


%build
%{__make} \
	MYCFLAGS="${RPM_OPT_FLAGS} -fPIC" \
	linux


%check
%{__make} test


%install
[ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != "/" ] && %{__rm} -rf ${RPM_BUILD_ROOT}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_prefix}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig

%{__make} \
	INSTALL_TOP=${RPM_BUILD_ROOT}%{_prefix} \
	install

%{__install} -m 0644 etc/lua.pc ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig

for PROG in ${RPM_BUILD_ROOT}%{_bindir}/{lua,luac}; do
  %{__mv}    -f      ${PROG}    ${PROG}%{maj}%{min}
done

for MANP in ${RPM_BUILD_ROOT}%{_mandir}/man1/{lua,luac}; do
  %{__mv}    -f      ${MANP}.1  ${MANP}%{maj}%{min}.1
done

# Cleanup
%{__rm} -f ${RPM_BUILD_ROOT}%{_libdir}/lib*.so.?


%post lib -p /sbin/ldconfig


%postun lib -p /sbin/ldconfig


%clean
[ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != "/" ] && %{__rm} -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc README doc/*.{css,gif,html,png}
%{_bindir}/lua%{maj}%{min}
%{_bindir}/luac%{maj}%{min}
%{_mandir}/man1/lua%{maj}%{min}.1*
%{_mandir}/man1/luac%{maj}%{min}.1*

%files devel
%defattr(-,root,root)
%{_includedir}/lauxlib.h
%{_includedir}/lua.h
%{_includedir}/lua.hpp
%{_includedir}/luaconf.h
%{_includedir}/lualib.h
%{_libdir}/liblua.so
%{_libdir}/pkgconfig/lua.pc

%files lib
%defattr(-,root,root)
%{_libdir}/liblua.so.*
%{_libdir}/lua
%{_datadir}/lua

%files static
%defattr(-,root,root)
%{_libdir}/liblua.a


%changelog
* Sat Feb 22 2014 Peter Pramberger <peterpramb@member.fsf.org> - 5.2.3-1
- Initial build
