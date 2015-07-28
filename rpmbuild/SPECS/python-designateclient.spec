%{!?__python2:        %define __python2 /usr/bin/python2}
%{!?python2_sitelib:  %define python2_sitelib  %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %define python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?python2_version:  %define python2_version  %(%{__python2} -c "import sys; sys.stdout.write(sys.version[:3])")}

Name:           python-designateclient
Version:        1.2.0
Release:        2%{?dist}
Summary:        Client library for OpenStack DNSaaS API

License:        ASL 2.0
URL:            http://wiki.openstack.org/designate
Source0:        https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python-pbr
Requires:       python-jsonschema
Requires:       python-keystoneclient
Requires:       python-requests
Requires:       python-six
Requires:       python-stevedore
Requires:       python-pbr

%description
Client library and command line utility for interacting with OpenStack DNSaaS API.

%prep
%setup -q
# Remove requirements listings
rm -rf {,test-}requirements.txt

# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%{__python2} -c 'import setuptools; execfile("setup.py")' build
##%%{__python2} setup.py build

%install
%{__python2} -c 'import setuptools; execfile("setup.py")' install \
	--skip-build -O1 --root ${RPM_BUILD_ROOT}
##%%{__python2} setup.py install --skip-build --root %%{buildroot}

%files 
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{python2_sitelib}/designateclient
%{python2_sitelib}/python_designateclient-%{version}-py?.?.egg-info
%{_bindir}/designate

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 29 2015 Victoria Martinez de la Cruz <vkmc@fedoraproject.com> - 1.2.0-1
- Update to 1.2.0.
* Mon Mar 30 2015 Victoria Martinez de la Cruz <vimartin@redhat.com> - 1.1.1-2
- Removes pbr patch.
* Wed Feb 25 2015 Victoria Martinez de la Cruz <vimartin@redhat.com> - 1.1.1-1
- Initial package.
