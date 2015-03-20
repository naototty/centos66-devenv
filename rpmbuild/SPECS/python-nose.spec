%{!?__python2:        %define __python2 /usr/bin/python2}
%{!?python2_sitelib:  %define python2_sitelib  %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %define python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?python2_version:  %define python2_version  %(%{__python2} -c "import sys; sys.stdout.write(sys.version[:3])")}

%define modn   nose
%define modv   1.3.4


Summary:       A discovery-based unittest extension for Python
Name:          python-%{modn}
Version:       %{modv}
Release:       1%{?dist}%{?pext}
License:       LGPL
Group:         Development/Libraries
Source0:       https://pypi.python.org/packages/source/n/%{modn}/%{modn}-%{modv}.tar.gz
Patch0:        %{modn}-1.3.4-install.patch
URL:           https://pypi.python.org/pypi/%{modn}/
Buildroot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Vendor:        Jason Pellerin <jpellerin@gmail.com>
Provides:      python(%{modn}) = %{modv}
Provides:      python(%{modn}.ext) = %{modv}
Provides:      python(%{modn}.plugins) = %{modv}
Provides:      python(%{modn}.sphinx) = %{modv}
Provides:      python(%{modn}.tools) = %{modv}
Requires:      python-setuptools
BuildRequires: python-devel >= 2.3 python-setuptools
BuildArch:     noarch


%description
Nose extends the test loading and running features of Python's unittest,
making it easier to write, find and run tests.


%prep
%setup -q -n %{modn}-%{modv}
%patch0 -p1


%build
%{__python2} -c 'import setuptools; execfile("setup.py")' build


%check
%{__python2} setup.py test


%install
[ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != "/" ] && %{__rm} -rf ${RPM_BUILD_ROOT}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_prefix}

%{__python2} -c 'import setuptools; execfile("setup.py")' install \
	--skip-build -O1 --root ${RPM_BUILD_ROOT}


%clean
[ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != "/" ] && %{__rm} -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc AUTHORS CHANGELOG NEWS README*
%doc lgpl.txt examples
%{_bindir}/nosetests
%{_bindir}/nosetests-%{python2_version}
%{python2_sitelib}/%{modn}
%{python2_sitelib}/*.egg-info
%{_mandir}/man1/nosetests.1*


%changelog
* Sun Jan 11 2015 Peter Pramberger <peterpramb@member.fsf.org> - 1.3.4-1
- Initial build
