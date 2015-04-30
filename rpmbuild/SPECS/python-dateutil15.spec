%global srcname python-dateutil
Name:           python-dateutil15
Version:        1.5
Release:        1%{?dist}
Summary:        Powerful extensions to the standard datetime module

Group:          Development/Languages
License:        Python
URL:            http://labix.org/python-dateutil
Source0:        http://labix.org/download/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel,python-setuptools

%description
The dateutil module provides powerful extensions to the standard datetime
module available in Python 2.3+.  This is a parallel installable newer version 
for EPEL 6 only.  RHEL 6 base has python-dateutil 1.4.1

%prep
%setup -q -n %{srcname}-%{version}
iconv --from=ISO-8859-1 --to=UTF-8 NEWS > NEWS.new
mv NEWS.new NEWS

%build
%{__python} setup.py bdist_egg

%install
mkdir -p %{buildroot}%{python_sitelib}
easy_install -m --prefix %{buildroot}%{_usr} dist/*.egg

chmod -x %{buildroot}%{python_sitelib}/python_dateutil-1.5-py2.?.egg/dateutil/*.py 
chmod -x %{buildroot}%{python_sitelib}/python_dateutil-1.5-py2.?.egg/dateutil/zoneinfo/__init__.py

%files
%doc example.py LICENSE NEWS README
%{python_sitelib}/python_dateutil-1.5-py2.?.egg

%changelog
* Wed Jul 13 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 1.5-1
- parallel installable newer version
- askbot indirectly requires this newer version via python-celery
